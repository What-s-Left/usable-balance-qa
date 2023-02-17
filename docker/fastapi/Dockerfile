ARG APP_HOME=/opt/src
ARG APP_UID="50000"
ARG APP_USER_HOME_DIR=/opt

ARG APT_DEPS="\
     apt-transport-https \
     apt-utils \
     build-essential \
     ca-certificates \
     libffi-dev \
     libkrb5-dev \
     libldap2-dev \
     libpq-dev \
     libsasl2-2 \
     libsasl2-dev \
     libsasl2-modules \
     libssl-dev \
     libxml2-dev \
     libxslt1-dev \
     zlib1g-dev \
     locales  \
     lsb-release \
     nodejs \
     openssh-client \
     postgresql-client \
     pkg-config \
     sasl2-bin \
     software-properties-common \
     sudo \
     openssl \
     libxmlsec1 \
     yarn"


# By default PIP has progress bar but you can disable it.
ARG PYTHON_VERSION="3.10"
ARG PYTHON_BASE_IMAGE="python:${PYTHON_VERSION}-slim"

# set environment variables  cvb hn
ARG PYTHONDONTWRITEBYTECODE=1
ARG PYTHONUNBUFFERED=1

FROM ${PYTHON_BASE_IMAGE} as usable-balance-connector-image

# Nolog bash flag is currently ignored - but you can replace it with
# xtrace - to show commands executed)
SHELL ["/bin/bash", "-o", "pipefail", "-o", "errexit", "-o", "nounset", "-o", "nolog", "-c"]

ARG PYTHON_BASE_IMAGE
ARG APT_DEPS

WORKDIR /opt/src

RUN apt-get update \
    && apt-get install --no-install-recommends -yqq apt-utils >/dev/null 2>&1 \
    && apt-get install -y --no-install-recommends curl gnupg2 \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
           ${APT_DEPS} \
    && apt-get autoremove -yqq --purge \
    && apt-get clean

ARG APP_HOME
ARG APP_USER_HOME_DIR
ARG APP_UID
ARG PYTHON_VERSION

RUN adduser --gecos "First Last,RoomNumber,WorkPhone,HomePhone" --disabled-password \
       --quiet "app" --uid "${APP_UID}" --gid "0" --home "${APP_USER_HOME_DIR}" && \
    mkdir -p ${APP_HOME} && chown -R "app:0" "${APP_USER_HOME_DIR}" ${APP_HOME}

RUN pip install --upgrade pip
COPY docker/fastapi/requirements.txt /opt/requirements.txt
RUN pip install --upgrade install -r /opt/requirements.txt

