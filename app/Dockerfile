FROM python:3.11

WORKDIR "/app"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1


COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY run.sh run.sh

COPY *.py ./

CMD ["bash", "run.sh", "prod"]