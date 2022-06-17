#!/usr/bin/env bash

php waitdb.php
echo VOU INSTALAR
php admin/cli/install_database.php --agree-license --adminuser=${CFG_ADMINUSER:-admin} --adminpass=${CFG_ADMINPASS:-admin} --adminemail=${CFG_ADMINEMAIL:-admin@server.local} --shortname=${CFG_SHORTNAME:-AVA-ZL} --fullname=${CFG_FULLNAME:-AVA_do_Zona_Leste} --summary=${CFG_FULLNAME:-AVA_do_Zona_Leste}
echo VOU ATUALIZAR
php admin/cli/upgrade.php --non-interactive --allow-unstable 
echo TUDO FEITO?
apache2-foreground