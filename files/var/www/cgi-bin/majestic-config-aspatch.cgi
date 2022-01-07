#!/bin/sh
time=$(date +"%s")
echo "Content-Type: text/plain"
echo "Content-Disposition: attachment; filename=\"majestic.${time}.patch\""
echo ""
diff /rom/etc/majestic.yaml /etc/majestic.yaml
