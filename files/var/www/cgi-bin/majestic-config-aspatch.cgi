#!/bin/sh

#payload=$(diff /rom/etc/majestic.yaml /etc/majestic.yaml)

time=$(date +"%s")
echo "Content-Type: text/plain"
#echo "Content-Length: ${#payload}"
echo "Content-Disposition: attachment; filename=\"majestic.${time}.patch\""
echo ""

diff /rom/etc/majestic.yaml /etc/majestic.yaml
