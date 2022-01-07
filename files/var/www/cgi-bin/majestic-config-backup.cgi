#!/bin/sh
file=/etc/majestic.yaml
echo "Content-Type: application/x-yaml"
echo "Content-Length: $(ls -l $file | xargs | cut -d " " -f 5)"
echo "Content-Encoding: gzip"
echo "Content-Disposition: attachment; filename=\"$(basename $file)\""
echo ""
gzip -c $file
