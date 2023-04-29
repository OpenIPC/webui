#!/bin/sh
preview=/tmp/preview.jpg
wget -q -O $preview http://127.0.0.1/image.jpg
if [ ! -f "$preview" ]; then
echo "HTTP/1.0 404"
else
echo "HTTP/1.1 200 OK
Content-type: image/jpeg
Content-Length: $(stat -c%s $preview)
Pragma: no-cache
Date: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Expires: $(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
Etag: \"$(cat /proc/sys/kernel/random/uuid)\"
Connecton: close
"
cat $preview
rm $preview
fi
