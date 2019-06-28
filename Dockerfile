FROM python:3-alpine
COPY . /app
WORKDIR /app
RUN apk add --update --no-cache ca-certificates && \
    pip --no-cache-dir --disable-pip-version-check install -r requirements.txt && \
    rm -rf /tmp/* /var/tmp/*
EXPOSE 33333
ENTRYPOINT ["/app/app.py"]
CMD []
