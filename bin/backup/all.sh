#!/bin/bash
source ../confs/enabled/db.env
eval "$(sentry-cli bash-hook)"

service=portal
tipo=ava

hoje=`date +'%Y_%m_%d'`
semana=`date +'%V'`
ano=`date +'%Y'`
mes=`date +'%m'`

backup_dir="/var/backups/portal"
backup_destin="backup:/ava/$service/$ano/$semana/"

mkdir -p $backup_dir

function targz_rclone() {
    subtipo=$1
    base_dir=$2
    backup_file="$backup_dir/$service.$subtipo.$hoje.tgz"

    tar -cvzf $backup_file -C $base_dir . \
    && rclone_backup_file $subtipo $backup_file \
    && rm $backup_file
}

function pgdump_rclone() {
    subtipo=$1
    container_backup_file="/var/lib/postgresql/data/$service.$subtipo.$hoje.pgdump"
    # backup_file="..//$service.$subtipo.$hoje.tgz"
    backup_file="../volumes/pgdata/$service.$subtipo.$hoje.pgdump"

    docker-compose exec -u postgres db pg_dumpall -U $POSTGRES_USER -f $container_backup_file \
    && rclone_backup_file $subtipo $backup_file \
    && rm $backup_file
}

function rclone_backup_file(){
    subtipo=$1
    backup_file=$2

    echo "Copiando $backup_file to $backup_destin"
    rclone copy $backup_file $backup_destin \
    && sentry-cli send-event -l info -m "Backup done: $service.$tipo" -m "Backup file: $backup_file" -t tipo:$tipo -t subtipo:$subitpo -t service:$service -t ano:$ano -t mes:$mes  -t semana:$semana
}

targz_rclone media /var/dockers/avaportal/volumes/media
pgdump_rclone sql
