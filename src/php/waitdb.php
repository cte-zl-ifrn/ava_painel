<?php
function env($name, $default=null) {
    return getenv($name, true) ?: $default;
}
function env_as_int($name, $default=null) {
    return intval(env($name, $default));
}
function env_as_bool($name, $default=null) {
    return intval(env($name, $default));
}

$dbhost = env('POSTGRES_HOST', 'db');
$dbname = env('POSTGRES_DATABASE', 'postgres');
$dbuser = env('POSTGRES_USER', 'ava_user');
$dbpass = env('POSTGRES_PASSWORD', 'ava_pass');
$dbport = env_as_int('POSTGRES_PORT', 5432);


$connected = false;
while (!$connected) {
    try {
        pg_connect("host={$dbhost} port={$dbport} dbname={$dbname} user={$dbuser} password={$dbpass}");
        $connected = true;
    } catch (Exception $e) {
        sleep(3);
    }
}
