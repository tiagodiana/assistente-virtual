FROM archlinux

RUN pacman -Syu  swig gcc make  libxrender espeak espeakup alsa-utils cmake  python-pip python-pkgconfig python-pkginfo --noconfirm




ADD . /assistente-virtual

RUN pip install --upgrade setuptools
RUN pip install --upgrade pyyaml
RUN pip install -r /assistente-virtual/requirements.txt

