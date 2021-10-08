# microbe-web

Microbe-WEB it is a simple and self-contained WEB interface based on [TBS](https://github.com/sayanriju/Tiny-Bash-Server)

-----

To start the old system, run two commands and put the files from the files_old directory in root folder

```
echo -e "#\nA:*\nD:*\n/cgi-bin:admin:12345\n#\n" >/tmp/httpd.conf

httpd -p "85" -h "/var/www" -c /tmp/httpd.conf -r "openipc"
```
