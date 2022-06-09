#!/bin/sh
time=$(date +"%s")
echo "Content-Type: text/plain
Content-Disposition: attachment; filename=\"majestic.${time}.patch\"
"
diff /rom/etc/majestic.yaml /etc/majestic.yaml
