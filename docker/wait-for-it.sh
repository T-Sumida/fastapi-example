#!/bin/sh

set -e

# 引数はdocker-compose.ymlで指定している。
# app:
#   ...
#   ..
#   .
#   entrypoint: /fastapi_sample/docker/wait-for-it.sh db 5432 postgres postgres db_fastapi_sample  # ココ
#   ...
host="$1"
shift
port="$1"
shift
user="$1"
shift
password="$1"
shift
database="$1"
shift
cmd="$@"

echo "Waiting for postgresql"
until pg_isready -h"$host" -U"$user" -p"$port" -d"$database"
do
  echo -n "."
  sleep 1
done

>&2 echo "PostgreSQL is up - executing command"
exec $cmd

# 僕は優しいのでMySQL用も書いてあげるのだ
#!/bin/sh

# set -e

# host="$1"
# shift
# user="$1"
# shift
# password="$1"
# shift
# cmd="$@"

# echo "Waiting for mysql"
# until mysqladmin ping -h "$host" --silent
# do
#     echo -n "."
#     sleep 1
# done

# >&2 echo "MySQL is up - executing command"
# exec $cmd