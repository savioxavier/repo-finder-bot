FROM python:3.10

RUN pip install -U \
    pip \
    setuptools \
    wheel

WORKDIR /repo-finder-bot

RUN useradd -m -r user && \
    chown user /repo-finder-bot

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

USER user

ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}

ENTRYPOINT ["/usr/local/bin/python3", "main.py"]