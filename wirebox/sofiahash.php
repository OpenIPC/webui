<?php
function sofiaHash(string $password): string
{
  $md5 = md5($password, true);
  return implode('', array_map(function ($i) use ($md5) {
    $c = (ord($md5[2 * $i]) + ord($md5[2 * $i + 1])) % 62;
    $c += $c > 9 ? ($c > 35 ? 61 : 55) : 48;
    return chr($c);
  }, range(0, 7)));
}
printf(sofiaHash('12345'));
?>
