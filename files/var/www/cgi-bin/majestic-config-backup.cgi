#!/bin/sh
file=/etc/majestic.yaml
echo "Content-Type: application/x-yaml
Content-Length: $(ls -l $file | xargs | cut -d " " -f 5)
Content-Encoding: gzip
Content-Disposition: attachment; filename=\"$(basename $file)\"
"
gzip -c $file
