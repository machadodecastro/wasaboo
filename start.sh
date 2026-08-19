#!/bin/bash
# Diretorio e arquivo de log
set -e
LOGFILE=/opt/myenv/wasaboo/logs/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
# Numero de processo simultaneo, modifique de acordo com seu processador
NUM_WORKERS=3
# Usuario/Grupo que vai rodar o gunicorn
USER=www-data
#GROUP=root
# Endereço local que o gunicorn irá rodar
ADDRESS=127.0.0.1:8000
# Ativando ambiente virtual e executando o gunicorn para este projeto
source /opt/myenv/wasaboo/bin/activate
cd /opt/myenv/wasaboo/wasaboo/
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn -w $NUM_WORKERS --bind=$ADDRESS --user=$USER --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE wasaboo.wsgi:application