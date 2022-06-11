#!/usr/bin/env bash

php waitdb.php
php admin/cli/install_database.php --agree-license --adminuser=${CFG_ADMINUSER:-'admin'} --adminpass=${CFG_ADMINPASS:-'admin'} --adminemail=${CFG_ADMINEMAIL:-'admin@server.local'} --fullname=${CFG_FULLNAME:-'AVA do Zona Leste'} --shortname=${CFG_FULLNAME:-'AVA-ZL'} --summary=${CFG_FULLNAME:-'Apenas para desenvolver o AVA do Zona Leste'}
php admin/cli/upgrade.php
apache2-foreground