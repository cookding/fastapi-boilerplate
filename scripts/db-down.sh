#!/bin/bash
set -ev

pushd `dirname $0`
docker compose down
popd
