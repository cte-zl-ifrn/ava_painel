# AVA - Portal

> Para este tutorial é subentendido que existe uma variável de ambiente $AP_HOME que aponta para a pasta raiz do projeto, a qual estará em `/var/dockers/avaportal/`.

```bash
# Baixe o projeto
git clone git@github.com:suap-ead/avaportal.git $AP_HOME

# Copie e edite as variáveis de ambiente
cd $AP_HOME
cp -r confs/examples confs/enabled
# vim confs/enabled/db.env
# vim confs/enabled/avaportal.env

# Instala o sistema
cd bin
./backs
./app/migrate
./app/manage createsuperuser

# Sobe o serviço
./app/up

# Se fores fazer um debug
# ./avaportal/debug
```

> Para agendar o backup pode ser utilizado o script `$AP_HOME/bin/backup/all.sh`. Ele irá requerer a instalação e configuração do rclone e do sentry-cli.

O serviço estará disponível em http://localhost:8080/ e será parecido com o que se vê abaixo:

![Alt text](screenshot.png?raw=true "Screenshot")
