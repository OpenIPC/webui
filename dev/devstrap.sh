#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 <last byte of IPC IP address>"
	exit
fi

IPC_IP="root@192.168.1.$1"

# copy ssh key
ssh-copy-id "$IPC_IP"

# copy dev configs
scp -O ../files/etc/init.d/S50httpd "${IPC_IP}:/etc/init.d/S50httpd"

# set env variable for dev web ui nfs share path
ssh "$IPC_IP" fw_setenv devnfs "$OPENIPC_WEBUI_DEV_SHARE"

# reboot
ssh "$IPC_IP" reboot -f

echo "Done"
exit 0
