FROM ctezlifrn/moodle:4.1.1-php8.0-014
ENV DEBIAN_FRONTEND noninteractive

COPY locale.gen /etc/locale.gen

USER root

RUN locale-gen && \
    dpkg-reconfigure locales && \
    apt install -y vim

COPY php-extra.ini /usr/local/etc/php/conf.d/extra.ini

USER www-data


WORKDIR /var/www/html/mod
RUN curl -o d.zip https://moodle.org/plugins/download.php/27960/mod_checklist_moodle41_2022111900.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/28434/mod_customcert_moodle41_2022041902.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/28300/mod_game_moodle41_2023010801.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27856/mod_mediagallery_moodle40_2022051101.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/28436/mod_attendance_moodle41_2023012601.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/28247/mod_offlinequiz_moodle40_2022111501.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27934/mod_coursecertificate_moodle41_2022111500.zip && unzip -o d.zip \
    && rm d.zip

# RUN curl -o d.zip https://moodle.org/plugins/download.php/28189/mod_bigbluebuttonbn_moodle311_2021101011.zip && unzip -o d.zip
# RUN curl -o d.zip https://moodle.org/plugins/download.php/28251/mod_hsuforum_moodle40_2022122100.zip && unzip -o d.zip
# RUN curl -o d.zip https://moodle.org/plugins/download.php/28179/mod_hvp_moodle41_2022121200.zip && unzip -o d.zip
# RUN curl -o d.zip https://moodle.org/plugins/download.php/27564/mod_journal_moodle40_2022091600.zip && unzip -o d.zip
# RUN curl -o d.zip https://moodle.org/plugins/download.php/26900/mod_questionnaire_moodle40_2021062301.zip && unzip -o d.zip
# RUN curl -o d.zip https://moodle.org/plugins/download.php/27665/mod_vpl_moodle40_2022093012.zip && unzip -o d.zip


WORKDIR /var/www/html/blocks
RUN curl -o d.zip https://moodle.org/plugins/download.php/27962/block_checklist_moodle41_2022111900.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/28052/block_completion_progress_moodle41_2022112800.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/26495/block_stash_moodle41_2022042100.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/28412/block_xp_moodle41_2022112610.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27924/block_game_moodle40_2022042733.zip && unzip -o d.zip \
    && rm d.zip


WORKDIR /var/www/html/mod/book/tool
RUN curl -o d.zip https://moodle.org/plugins/download.php/25049/booktool_wordimport_moodle41_2021083100.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/11995/booktool_exportepub_moodle31_2016081500.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/15925/booktool_importepub_moodle34_2018020100.zip && unzip -o d.zip \
    && rm d.zip


WORKDIR /var/www/html/filter
RUN curl -o d.zip https://moodle.org/plugins/download.php/24270/filter_syntaxhighlighter_moodle41_2021052101.zip && unzip -o d.zip \
    && rm d.zip
# RUN curl -o d.zip https://moodle.org/plugins/download.php/24512/filter_h5p_moodle311_2021062200.zip && unzip -o d.zip


WORKDIR /var/www/html/lib/editor/atto/plugins
RUN curl -o d.zip https://moodle.org/plugins/download.php/9418/atto_chemistry_moodle31_2015092900.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/17250/atto_count_moodle35_2018062700.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/9419/atto_computing_moodle30_2015092900.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/17168/atto_justify_moodle40_2018041600.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/24509/atto_morebackcolors_moodle41_2021062100.zip && unzip -o d.zip && mv ndunand-moodle-atto_morebackcolors-* morebackcolors \
    && curl -o d.zip https://moodle.org/plugins/download.php/24505/atto_morefontcolors_moodle41_2021062100.zip && unzip -o d.zip && mv ndunand-moodle-atto_morefontcolors-* morefontcolors \
    && rm d.zip


WORKDIR /var/www/html/enrol
RUN curl -o d.zip https://moodle.org/plugins/download.php/21447/enrol_xp_moodle41_2020042901.zip && unzip -o d.zip \
    && rm d.zip


WORKDIR /var/www/html/admin/tool
RUN curl -o d.zip https://moodle.org/plugins/download.php/26575/tool_bulkchangeprofilefields_moodle40_2022042900.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/28188/tool_clearbackupfiles_moodle41_2022121200.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27662/tool_coursearchiver_moodle40_2022100400.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/18375/tool_hidecourses_moodle41_2018112800.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/23370/tool_ribbons_moodle310_2021020400.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27931/tool_certificate_moodle41_2022111500.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27935/tool_datewatch_moodle41_2022111500.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/24851/tool_uploadenrolmentmethods_moodle40_2021080201.zip && unzip -o d.zip \
    && rm d.zip


WORKDIR /var/www/html/availability/condition
RUN curl -o d.zip https://moodle.org/plugins/download.php/22786/availability_xp_moodle41_2020110900.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/26314/availability_coursecompleted_moodle41_2022040400.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27159/availability_role_moodle40_2022071200.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/26482/availability_language_moodle41_2022041900.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/24360/availability_mobileapp_moodle311_2021060200.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27155/availability_cohort_moodle40_2022071200.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27188/availability_password_moodle40_2022071200.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/16615/availability_stash_moodle41_2018050901.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/25682/availability_othercompleted_moodle311_2021112500.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/11311/availability_badge_moodle31_2016020200.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/16249/availability_enrol_moodle34_2018030900.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/24334/availability_sectioncompleted_moodle40_2021052800.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/16001/availability_maxviews_moodle311_2018020600.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/23733/availability_quizquestion_moodle311_2021031700.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/22196/availability_courseprogress_moodle310_2020070100.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/26564/availability_game_moodle40_2022042610.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/26392/availability_user_moodle41_2022040801.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27907/availability_relativedate_moodle41_2022111100.zip && unzip -o d.zip \
    && rm d.zip

# RUN curl -o d.zip https://moodle.org/plugins/download.php/17146/availability_days_moodle35_2016060100.zip && unzip -o d.zip
# RUN curl -o d.zip https://moodle.org/plugins/download.php/12250/availability_week_moodle31_2016060100.zip && unzip -o d.zip
# RUN curl -o d.zip https://moodle.org/plugins/download.php/23689/availability_enroldate_moodle41_2020061500.zip && unzip -o d.zip
# RUN curl -o d.zip https://moodle.org/plugins/download.php/15953/availability_dataformcontent_moodle33_2017051502.zip && unzip -o d.zip


WORKDIR /var/www/html/report
RUN curl -o d.zip https://moodle.org/plugins/download.php/25665/report_extendedlog_moodle311_2021121302.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/24073/report_overviewstats_moodle311_2021050500.zip && unzip -o d.zip \
    && rm d.zip


WORKDIR /var/www/html/course/format
RUN curl -o d.zip https://moodle.org/plugins/download.php/28461/format_tiles_moodle41_2023013000.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/26671/format_remuiformat_moodle40_2022120500.zip && unzip -o d.zip \
    && rm d.zip


WORKDIR /var/www/html/theme
RUN curl -o d.zip https://moodle.org/plugins/download.php/28087/theme_moove_moodle41_2022112801.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/28046/theme_adaptable_moodle41_2022112300.zip && unzip -o d.zip \
    && rm d.zip

# theme_aberto v3.11 2021052101
# theme_ead v38-r1 2020072901
# theme_ledor  2020081301


WORKDIR /var/www/html/local
RUN curl -o d.zip https://moodle.org/plugins/download.php/21216/local_analytics_moodle38_2019070801.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/28080/local_cohortrole_moodle41_2022112900.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/28172/local_mailtest_moodle41_2022121100.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27251/local_maintenance_livecheck_moodle40_2022071200.zip && unzip -o d.zip \
    && rm d.zip

# local_suap 0.2.007 20221229007


WORKDIR /var/www/html/grade/export
RUN curl -o d.zip https://moodle.org/plugins/download.php/27963/gradeexport_checklist_moodle41_2022111900.zip && unzip -o d.zip \
    && rm d.zip


WORKDIR /var/www/html/user/profile/field
RUN curl -o d.zip https://moodle.org/plugins/download.php/5944/profilefield_cpf_moodle310_2014041700.zip && unzip -o d.zip \
    && sed -i 's/\$cpf{\$c}/$cpf[$c]/g' /var/www/html/user/profile/field/cpf/field.class.php \
    && curl -o d.zip https://moodle.org/plugins/download.php/27125/profilefield_autocomplete_moodle311_2022071900.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/26013/profilefield_timestamp_moodle311_2022021700.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/22197/profilefield_masked_moodle310_2020080800.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/13216/profilefield_dynamicmultiselect_moodle32_2017021201.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/28148/profilefield_brasilufmunicipio_moodle41_2022120600.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/13215/profilefield_dynamicmenu_moodle32_2017021201.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/21799/profilefield_multiselect_moodle39_2020061800.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/23487/profilefield_associated_moodle310_2021021600.zip && unzip -o d.zip \
    # && curl -o d.zip https://moodle.org/plugins/download.php/25909/profilefield_conditional_moodle311_2022012800.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/26428/profilefield_statictext_moodle40_2022041200.zip && unzip -o d.zip \
    && curl -o d.zip https://moodle.org/plugins/download.php/27042/profilefield_orcid_moodle40_2022070900.zip && unzip -o d.zip \
    && rm d.zip

# profile_field_dynamicmenu::__construct() must support $fielddata as the third argument and pass it to the parent constructor
# line 103 of /user/profile/lib.php: call to debugging()
# line 53 of /user/profile/field/dynamicmenu/field.class.php: call to profile_field_base->__construct()
# line 613 of /user/profile/lib.php: call to profile_field_dynamicmenu->__construct()
# line 684 of /user/profile/lib.php: call to profile_get_user_fields_with_data()
# line 242 of /user/editadvanced_form.php: call to profile_definition_after_data()
# line 1024 of /lib/formslib.php: call to user_editadvanced_form->definition_after_data()
# line 360 of /user/editadvanced.php: call to moodleform->display()
# profile_field_dynamicmultiselect::__construct() must support $fielddata as the third argument and pass it to the parent constructor
# line 103 of /user/profile/lib.php: call to debugging()
# line 55 of /user/profile/field/dynamicmultiselect/field.class.php: call to profile_field_base->__construct()
# line 613 of /user/profile/lib.php: call to profile_field_dynamicmultiselect->__construct()
# line 684 of /user/profile/lib.php: call to profile_get_user_fields_with_data()
# line 242 of /user/editadvanced_form.php: call to profile_definition_after_data()
# line 1024 of /lib/formslib.php: call to user_editadvanced_form->definition_after_data()
# line 360 of /user/editadvanced.php: call to moodleform->display()


# WORKDIR /var/www/html/theme
# RUN curl -o d.zip https://moodle.org/plugins/download.php/28087/theme_moove_moodle41_2022112801.zip && unzip -o d.zip \
#     && rm d.zip


# WORKDIR /var/www/html/
# RUN curl https://codeload.github.com/cte-zl-ifrn/moodle__local_suap/tar.gz/refs/tags/0.2.025 | tar -zx && mv moodle__local_suap-* local/suap \
#     && curl https://codeload.github.com/cte-zl-ifrn/moodle__block_suapattendance/tar.gz/refs/tags/0.1.0 | tar -zx && mv moodle__block_suapattendance-* blocks/suapattendance


USER www-data
WORKDIR /var/www/html
EXPOSE 80
# ENTRYPOINT ["docker-php-entrypoint"]


