FROM skyfarer/ecmwf-eccodes
RUN apk update && apk add nodejs npm aws-cli bash
RUN mkdir /app
WORKDIR /app/
RUN npm install ioredis ngeohash
COPY scripts/* /app/
