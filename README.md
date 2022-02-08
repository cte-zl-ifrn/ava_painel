# AVA - Portal

```bash
# Baixe o projeto
git clone git@github.com:suap-ead/avaportal.git avaportal

# Copie e edite as variáveis de ambiente
cd avaportal
cp -r confs/examples confs/enabled
# vim confs/enabled/db.env
# vim confs/enabled/avaportal.env

# Instala o sistema
cd bin
./backs
./app/migrate
./app/debug

```


> O serviço estará disponível em http://localhost:7002/ e será parecido com o que se vê abaixo:
