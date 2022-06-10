# FROM moodlehq/moodle-php-apache:8.1-bullseye # not for production
FROM moodlehq/moodle-php-apache:7.4

ENV DEBIAN_FRONTEND noninteractive

RUN curl -L -o v.tar.gz https://github.com/moodle/moodle/archive/refs/tags/v3.11.7.tar.gz \
    && tar -zxf v.tar.gz \
    && rm v.tar.gz \
    && mv moodle-3.11.7/* /var/www/html/ \
    && chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && mkdir /var/custom_logs/ \
    && chown -R www-data:www-data /var/custom_logs/ \
    && curl --silent --show-error https://getcomposer.org/installer | php \ 
    && mv composer.phar /usr/bin/composer

ADD config.php /var/www/html/config.php

# VOLUME [ "/var/moodledata/antivirus_quarantine", "/var/moodledata/cache", "/var/moodledata/filedir", "/var/moodledata/lang", "/var/moodledata/localcache", "/var/moodledata/lock", "/var/moodledata/muc", "/var/moodledata/sessions", "/var/moodledata/temp", "/var/moodledata/trashdir" ]
# EXPOSE 80
# ENTRYPOINT ["docker-php-entrypoint"]
CMD php admin/cli/install_database.php --agree-license --adminuser={CFG_ADMINUSER:-admin} --adminpass=${CFG_ADMINPASS:-admin} --adminemail=${CFG_ADMINEMAIL:-admin@server.local} --fullname=${CFG_FULLNAME:-AVA-do-Zona-Leste} --shortname=${CFG_FULLNAME:-AVA-ZL} --summary=${CFG_FULLNAME:-AVA-do-Zona-Leste} ; php admin/cli/upgrade.php ; apache2-foreground