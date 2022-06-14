#!/usr/bin/env bash

php waitdb.php
php admin/cli/install_database.php --agree-license --adminuser=${CFG_ADMINUSER:-admin} --adminpass=${CFG_ADMINPASS:-admin} --adminemail=${CFG_ADMINEMAIL:-admin@server.local} --shortname=${CFG_SHORTNAME:-AVA-ZL} --fullname=${CFG_FULLNAME:-AVA_do_Zona_Leste} --summary=${CFG_FULLNAME:-AVA_do_Zona_Leste}
php admin/cli/upgrade.php --non-interactive --allow-unstable 
apache2-foreground