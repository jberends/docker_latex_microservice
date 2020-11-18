FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV DEBIAN_FRONTEND noninteractive
ENV APT_CACHE_DIR /.apt_cache
RUN mkdir $APT_CACHE_DIR
RUN apt-get update && \
    apt-get install -o dir::cache::archives="$APT_CACHE_DIR" -y \
    texlive \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    texlive-latex-extra \
    texlive-xetex \
    texlive-luatex \
    texlive-lang-english \
    texlive-lang-german \
    texlive-lang-french
RUN rm -rf /var/lib/apt/lists/* && rm -rf $APT_CACHE_DIR

# prep App
RUN mkdir /workspace

## do virtualenv installation
COPY ./requirements.txt /requirements.txt
RUN pip install -U -r /requirements.txt


