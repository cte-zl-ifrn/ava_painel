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
