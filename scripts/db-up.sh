#!/bin/bash
set -ev

pushd `dirname $0`

docker compose up -d

STATUS=""
until [[ ${STATUS} = "/var/run/postgresql:5432 - accepting connections" ]]; do
    sleep 3
    STATUS=`docker exec postgres pg_isready || true`
    echo ${STATUS}
done

popd
