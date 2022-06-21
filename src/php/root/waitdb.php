<?php
define('CLI_SCRIPT', true);
define('CACHE_DISABLE_ALL', true);
echo "VAMOS LÁ\n";

$connected = false;
$i = 1;
while (!$connected) {
    echo "Tentando conectar: $i ... ";
    try {
        require_once(__DIR__ . '/config.php');
        global $DB;
        if ($DB->get_record_sql('select 2 check')->check == 2) {
            $connected = true;
            sleep(3);
            echo "CONNECTED.\n";
        };
    } catch(Exception $e) {
        echo "NOT CONNECTED.\n";
        sleep(3);
        $i++;        
    }
}
