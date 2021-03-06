FROM ubuntu:latest as image

RUN apt-get update -yq && \
	apt-get install ca-certificates -y

RUN echo "deb [trusted=true] https://packages.twingate.com/apt/ /" | tee /etc/apt/sources.list.d/twingate.list


RUN apt-get update -yq && \
    apt-get install -yd twingate

RUN cp /var/cache/apt/archives/twingate_0.49.0_amd64.deb /tmp/ && \
    ls -l /tmp/


FROM archlinux:latest

RUN pacman -Syy && \
    pacman -S --noconfirm git base-devel go

RUN git clone https://aur.archlinux.org/yay.git && \
    useradd -m -G wheel cloudcone && \
    chown -R cloudcone:adm yay && \
    gpasswd -a cloudcone adm && \
    echo "cloudcone ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    su -l cloudcone

USER cloudcone

RUN cd yay && \
    sudo -u cloudcone makepkg -sif --noconfirm

RUN sudo -u cloudcone yay -S --noconfirm debtap

RUN sudo debtap -u

COPY --from=image /tmp/* /tmp/

RUN sudo debtap /tmp/twingate_0.49.0_amd64.deb

RUN find / -name twingate*