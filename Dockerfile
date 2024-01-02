FROM python:3.11-alpine as builder

RUN set -xe \
    && apk upgrade \
    && apk add --no-cache gcc g++ musl-dev openssl-dev \
    && pip3 install --upgrade setuptools pip

COPY ./llmchatbot/ /install

RUN set -xe \
    && pip3 install --prefix="/install" --no-warn-script-location /install/

FROM python:3.11-alpine

COPY --from=builder /install /usr/local
COPY --from=builder /usr/lib/ /usr/lib/

RUN set -ex \
    && addgroup -g 96 -S python-user \
    && adduser --uid 96 -D -S --ingroup python-user python-user

USER python-user:python-user

ARG BUILD_VERSION
ARG BUILD_COMMIT_SHA
ARG BUILD_CREATION_DATE
ARG BUILD_URL
ARG BUILD_CLONE_URL

ENV PYTHONUNBUFFERED=1
ENV BUILD_VERSION=${BUILD_VERSION}

LABEL org.opencontainers.image.title="llmchatbot"
LABEL org.opencontainers.image.description="Generate LLM Chatbot from a Website's URL"
LABEL org.opencontainers.image.version=${BUILD_VERSION}
LABEL org.opencontainers.image.created=${BUILD_CREATION_DATE}
LABEL org.opencontainers.image.revision=${BUILD_COMMIT_SHA}
LABEL org.opencontainers.image.url=${BUILD_CLONE_URL}
LABEL org.opencontainers.image.source=${BUILD_URL}

ENTRYPOINT [ "llmchatbot" ]