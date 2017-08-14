#!/usr/bin/env python3

from argparse import ArgumentParser
from ast import alias, Import, ImportFrom, Module, parse
from contextlib import contextmanager
from json import dumps
from logging import basicConfig, INFO, getLogger
from os import chdir, getcwd, getenv, listdir
from os.path import basename, exists, join, isfile
from pip.wheel import Wheel
from requests import get, codes, session
from requests_toolbelt.multipart import MultipartEncoder
from subprocess import check_output, CalledProcessError, STDOUT
from sys import path

logging = basicConfig(
    format='%(asctime)-15s %(levelname)-6s %(message)s',
    level=INFO
)
logger = getLogger('wheel-builder')

class Distribution(object):
    def __init__(self, source):
        self._source = source

        # Contains every key-value pair passed into the
        # setup function in setup.py even though this
        # object is only exposing a sub-set of values
        self._setup_params = self.parse_setup_py()

    @property
    def source(self):
        return self._source

    @property
    def name(self):
        return self._setup_params['name']

    @property
    def version(self):
        return self._setup_params['version']

    @property
    def install_deps(self):
        if 'install_requires' in self._setup_params:
            return self._setup_params['install_requires']
        else:
            return []
    @property
    def test_deps(self):
        if 'tests_require' in self._setup_params:
            return self._setup_params['tests_require']
        else:
            return []

    def parse_setup_py(self):
        with Distribution.cd(self.source):
            global setup_params
            setup_params = {}

            setup_py = join('.', 'setup.py')
            if not exists(setup_py):
                logger.error('build failed reason=no setup.py found in path %s', self.source)
                exit(1)

            __file__ = setup_py

            source_str = ""
            with open(setup_py) as inf:
                source_str = inf.read()

            tree = parse(source_str)

            for node in tree.body:
                if not (isinstance(node, Import) or isinstance(node, 
                    ImportFrom) or isinstance(node, alias)):
                    continue

                wrapper = Module(body=[node])
                co = compile(wrapper, "<ast>", "exec")
                exec(co)

            # Redefining the setup function at this point after all definitions
            # have been parsed and are available for execution of the rest of
            # the setup.py script.
            def setup(*args, **kwargs):
                global setup_params
                setup_params = kwargs

            for node in tree.body:
                if isinstance(node, Import) or isinstance(node, 
                    ImportFrom) or isinstance(node, alias):
                    continue

                wrapper = Module(body=[node])
                co = compile(wrapper, "<ast>", "exec")
                exec(co, locals())

        return setup_params

    @staticmethod
    @contextmanager
    def cd(new_dir):
        old_dir = getcwd()
        chdir(new_dir)
        path.insert(0, getcwd())
        try:
            yield
        finally:
            path.pop(0)
            chdir(old_dir)


class PackageList(object):
    def __init__(self, path='', url='', useURL=True):
        self.default_url = ''
        self.default_path = '/tmp/package_list.txt'

        self._path = path if path else self.default_path
        self._url = url if url else self.default_url
        self._useURL = useURL
        self.get_list()

    def get_list(self):
        pkg_list = self.get_list_from_path()
        from_path = True

        if self.useURL:
            url_pkg_list = self.get_list_from_url()

            if url_pkg_list:
                pkg_list = url_pkg_list
                from_path = False

        pkg_list = [PackageList.normalize(name) for name in pkg_list]
        self._package_list = pkg_list
        self._is_from_path = from_path

    def get_list_from_url(self):
        pkg_list = []

        try:
            r = get(self.url)
            if r.status_code == codes.ok:
                lines = r.text.split("\n")
                pkg_list = [PackageList.normalize(l) for l in lines]
            else:
                raise Exception("error retrieving url")
        except:
            logger.error('error retrieving package list from url %s', self.url)
        finally:
            return pkg_list
        
    def get_list_from_path(self):
        if not exists(self.path):
            logger.error('build failed reason=no package_list found in path %s', self.path)
            exit(1)

        with open(self.path, 'r') as inf:
            lines = inf.readlines()
        lines = [ l.strip() for l in lines]
        return lines
        
    @property
    def package_list(self):
        return self._package_list
    
    @property
    def url(self):
        return self._url
    
    @property
    def path(self):
        return self._path

    @property
    def useURL(self):
        return self._useURL

    @property
    def is_from_path(self):
        return self._is_from_path
    
    @property
    def is_from_url(self):
        return not self.is_from_path
    
    @property
    def is_modified(self):
        return self._is_modified

    def is_member(self, pkg):
        name = PackageList.get_name(pkg)
        return name in self.package_list

    @staticmethod
    def get_name(pkg_req):
        split_chars = ['<', '>', '=', '!']

        name = pkg_req

        for char in split_chars:
            if char in pkg_req:
                tokens = pkg_req.split(char)
                name = tokens[0]
                break
    
        return PackageList.normalize(name)

    @staticmethod
    def normalize(pkg_name):
        # Per PEP 426
        return pkg_name.strip().lower().replace("-", "_")


class WheelBuilder(object):
    def __init__(self, source, wheelhouse, host, username, password, no_external, no_test_deps):
        self._session = None
        self._source = source
        self._wheelhouse = wheelhouse
        self._host = host
        self._username = username
        self._password = password
        self._no_external = no_external
        self._no_test_deps = no_test_deps

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def source(self):
        return self._source

    @property
    def wheelhouse(self):
        return self._wheelhouse

    @property
    def no_external(self):
        return self._no_external

    @property
    def no_test_deps(self):
        return self._no_test_deps

    @property
    def index_host(self):
        return self._host

    @property
    def index_url(self):
        return 'https://{0}:{1}@{2}/simple'.format(
            self.username, self.password, self.index_host)

    @property
    def upload_url(self):
        return 'https://{}/'.format(self.index_host)

    @property
    def extra_index(self):
        return 'https://pypi.python.org/simple'

    @property
    def session(self):
        if self._session is None:
            self._session = session()
            self._session.auth = (self.username, self.password)
        return self._session

    def upload(self):
        for filename in listdir(self.wheelhouse):
            filepath = join(self.wheelhouse, filename)
            if isfile(filepath) and filename.endswith('.whl'):
                try:
                    self.upload_wheel(filepath)
                except Exception as e:
                    logger.error('upload failed wheel=%s reason=%s', filepath, e.message)

    def upload_wheel(self, filepath):
        filename = basename(filepath)
        wheel = Wheel(filepath)
        logger.info('uploading wheel=%s', filepath)
        with open(filepath, 'rb') as f:
            data = {
                ':action': 'file_upload',
                'protcol_version': '1',
                'name': basename(wheel.name),
                'version': wheel.version,
                'content': (filename, f, 'application/octet-stream')
            }
            encoder = MultipartEncoder(data.items())
            response = self.session.post(
                self.upload_url,
                data=encoder,
                allow_redirects=False,
                headers={'Content-Type': encoder.content_type},
                verify=False,
                timeout=90.0
            )
        if response.status_code == 200:
            logger.info('upload completed: %s', dumps(response.json(), indent=2))
        else:
            logger.error('unexpected status=%s received along with response=\n%s', response.status_code, response.content)
        return response

    def build(self):
        self.build_wheel(self.source)


    def build_deps(self):
        dist = Distribution(self.source)
        deps = dist.install_deps

        if not self.no_test_deps:
            deps.extend(dist.test_deps)

        pkg_list = PackageList()

        exclude = lambda dep: False if dep.find("!") < 0 else True

        for dep in deps:
            if exclude(dep):
                continue

            if pkg_list.is_member(dep):
                self.build_wheel(dep, no_deps=False, no_external=True)
            else:
                self.build_wheel(dep, no_deps=False, no_external=self.no_external)


    def build_wheel(self, source, no_deps=True, no_external=False):
        cmd = [
            'pip3',
            'wheel',
            '--trusted-host={0}'.format(self.index_host),
            '--index-url={0}'.format(self.index_url),
            '--wheel-dir={0}'.format(self.wheelhouse),
            source
        ]

        if no_deps == True:
            cmd.insert(-1, '--no-deps')

        if no_external == False:
            cmd.insert(-1, '--extra-index-url={0}'.format(self.extra_index))

        try:
            logger.info('building wheel source=%s wheelhouse=%s', source, self.wheelhouse)
            logger.debug('executing command=%s', ' '.join(cmd))
            check_output(cmd, stderr=STDOUT)
            logger.info('building completed')
        except CalledProcessError as e:
            logger.error('build failed reason=%s', e.output)
            exit(1)


def parse_opts():
    parser = ArgumentParser(description='Wheel Builder CLI')

    parser.add_argument('-s', '--source', help='source directory', default=getenv('SOURCES', '/sources'))
    parser.add_argument('-w', '--wheelhouse', help='wheelhouse directory', default=getenv('WHEELHOUSE', '/wheelhouse'))

    pypi_group = parser.add_argument_group()
    pypi_group.add_argument('-u', '--username', help='pypi repository username',
                            default=getenv('PYPI_USERNAME', 'pypi_username'))
    pypi_group.add_argument('-p', '--password', help='pypi repository password', default=getenv('PYPI_PASSWORD', None))
    pypi_group.add_argument('-H', '--host', help='pypi index host', default=getenv('PYPI_URL', 'pypi.python.org'))

    deps_group = parser.add_mutually_exclusive_group()
    deps_group.add_argument('-D', '--no-deps', help='skip dependencies', action='store_true', default=False)
    deps_group.add_argument('-P', '--no-package', help='skip package', action='store_true', default=False)

    parser.add_argument('-X', '--no-external', help='do not use external PyPI repo', action='store_true', default=False)
    parser.add_argument('-T', '--no-test-deps', help='skip testing dependencies', action='store_true', default=False)

    upload_group = parser.add_mutually_exclusive_group()
    upload_group.add_argument('-U', '--upload', help='upload built wheels', action='store_true', default=False)

    args = vars(parser.parse_args())

    if args['password'] is None:
        parser.error('PYPI_PASSWORD is not set nor explicitly passed in via -p/--password')
        exit(1)

    return args


def main():
    args = parse_opts()
    builder = WheelBuilder(
        source=args['source'],
        wheelhouse=args['wheelhouse'],
        host=args['host'],
        username=args['username'],
        password=args['password'],
        no_external=args['no_external'],
        no_test_deps=args['no_test_deps']
    )

    if not args['no_package']:
        builder.build()

    if not args['no_deps']:
        builder.build_deps()

    if args['upload']:
        builder.upload()

if __name__ == '__main__':
    main()
