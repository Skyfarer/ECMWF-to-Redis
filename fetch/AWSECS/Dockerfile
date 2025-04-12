FROM alpine
RUN apk update && apk add bash aws-cli
COPY fetch_ecmwf.sh /app/
WORKDIR /app
ENTRYPOINT ./fetch_ecmwf.sh
