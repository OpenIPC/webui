#!/bin/sh

config_file=/etc/coredump.conf
admin_file=/etc/webui/admin.conf
core_file=dump.core
info_file=info.txt

LOG_FILE=/root/coredump.log
:>$LOG_FILE

log "Majectic crashed"

log() {
	local txt="$(date +"%F %T") [${PID}] ${1}"
	echo "$txt" >>$LOG_FILE
	[ "1" != "$quiet" ] && echo "$txt"
	unset txt
}

[ ! -f "$config_file" ] && log "Config file ${config_file} not found." && exit 1
source "$config_file"

[ ! -f "$admin_file" ] && log "Admin config file ${admin_file} not found." && exit 2
source "$admin_file"

[ "true" != "$coredump_enabled" ] && log "Core dump not enabled." && exit 3

log "Stopping watchdog"
rmmod wdt
log "done"

cd /tmp

log "Dumping core"
cat /dev/stdin >$core_file
log "done"

bundle_name=$(ifconfig -a | grep HWaddr | sed s/.*HWaddr// | sed "s/[: ]//g" | uniq)-$(date +"%Y%m%d-%H%M%S").tgz

# FIXME: can be read from /tmp/sysinfo.txt
soc=$(ipcinfo --chip-name)
family=$(ipcinfo --family)
vendor=$(ipcinfo --vendor)
sensor=$(ipcinfo --long-sensor)
mac=$(ipcinfo --xm-mac)
os=$(cat /etc/os-release)
mj=$(majestic -v)

:>$info_file
echo "
Date: $(TZ=GMT0 date)
Name: ${admin_name}
Email: ${admin_email}
Telegram: ${admin_telegram}

Hardware:
---------
SoC: ${soc}
Family: ${family}
Vendor: ${vendor}
Sensor: ${sensor}
MAC: ${mac}

Firmware:
---------
${os}
MAJESTIC_VERSION=\"${mj}\"
" >>$info_file

cat /etc/majestic.yaml >majestic.yaml

log "Creating bundle"
tar c -h "$core_file" "$info_file" majestic.yaml | gzip >"$bundle_name"
log "done"

rm "$core_file" "$info_file" majestic.yaml

if [ "true" = "$coredump_send2devs" ]; then
	log "Sending to S3 bucket"
	curl --silent --verbose "https://majdumps.s3.eu-north-1.amazonaws.com/${bundle_name}" --upload-file "$bundle_name" >>$LOG_FILE
	log "done"
fi

if [ "true" = "$coredump_send2tftp" ]; then
	log "Sending to TFTP server"
	tftp -p -l "$bundle_name" $coredump_tftphost >>$LOG_FILE
	log "done"
fi

if [ "true" = "$coredump_send2ftp" ]; then
	log "Sending to FTP server"
	curl --silent --verbose "ftp://${coredump_ftphost}/${coredump_ftppath}/" --upload-file "$bundle_name" --user "${coredump_ftpuser}:${coredump_ftppass}" --ftp-create-dirs >>$LOG_FILE
	log "done"
fi

if [ "true" = "$coredump_save4web" ]; then
	[ -z "$coredump_localpath" ] && coredump_localpath="/root"
	[ ! -d "$coredump_localpath" ] && mkdir -p "$coredump_localpath"
	log "Saving locally to ${coredump_localpath}/coredump.tgz"
	mv "$bundle_name" "${coredump_localpath}/coredump.tgz"
	log "done"
else
	rm "$bundle_name"
fi

[ "1" = "$verbose" ] && cat $LOG_FILE

log "All done. Rebooting..."
umount -a -t nfs -l
reboot -f
