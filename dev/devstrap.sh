#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 <last byte of IPC IP address>"
	exit
fi

IPC_IP="root@192.168.1.$1"

echo "Copy SSH key"
ssh-copy-id "$IPC_IP"

echo "Copy dev configs"
scp -O ../files/etc/init.d/S50httpd "${IPC_IP}:/etc/init.d/S50httpd"

echo "Set env variable for dev Web UI NFS share path"
ssh "$IPC_IP" "fw_setenv devnfs $OPENIPC_WEBUI_DEV_SHARE"

echo "Reboot"
ssh "$IPC_IP" reboot -f

echo "Done"
exit 0
