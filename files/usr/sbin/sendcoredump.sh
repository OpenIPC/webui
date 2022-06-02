#!/bin/sh

conf_file=/etc/coredump.config
core_file=dump.core
info_file=info.txt

if [ ! -f "$conf_file" ]; then
  echo "Config file ${conf_file} not found."
  exit 1
fi

if [ ! "$(grep ^savedumps $conf_file | cut -d= -f2)" == "true" ]; then
  echo "Core dump not enabled."
  exit 2
fi

cd /tmp

cat /dev/stdin > $core_file

bundle_name=$(ifconfig -a | grep HWaddr | sed s/.*HWaddr// | sed "s/[: ]//g" | uniq)-$(date +"%Y%m%d-%H%M%S").tgz

name=$(grep ^contact_name $conf_file | cut -d= -f2)
email=$(grep ^contact_email $conf_file | cut -d= -f2)
telegram=$(grep ^contact_telegram $conf_file | cut -d= -f2)
soc=$(ipcinfo --chip-name)
family=$(ipcinfo --family)
vendor=$(ipcinfo --vendor)
sensor=$(ipcinfo --long_sensor)
mac=$(ipcinfo --xm-mac)
os=$(cat /etc/os-release)
mj=$(majestic -v)

:>$info_file
echo -e "Date: $(TZ=GMT date)\nName: ${name}\nEmail: ${email}\nTelegram: ${telegram}\n" >> "$info_file"
echo -e "Hardware:\n---------\nSoC: ${soc}\nFamily: ${family}\nVendor: ${vendor}\nSensor: ${sensor}\nMAC: ${mac}\n" >> "$info_file"
echo -e "Firmware:\n---------\n${os}\nMAJESTIC_VERSION=\"${mj}\"\n" >> "$info_file"

cat /etc/majestic.yaml > majestic.yaml

tar c -h "$core_file" "$info_file" majestic.yaml | gzip > "$bundle_name"
rm "$core_file" "$info_file" majestic.yaml

if [ "$(grep ^send2tftp $conf_file | cut -d= -f2)" == "true" ]; then
  tftphost=$(grep ^tftphost $conf_file | cut -d= -f2)
  tftp -p -l "$bundle_name" $tftphost
fi

if [ "$(grep ^send2devs $conf_file | cut -d= -f2)" == "true" ]; then
  curl -s "https://majdumps.s3.eu-north-1.amazonaws.com/${bundle_name}" --upload-file "$bundle_name"
fi

if [ "$(grep ^send2ftp $conf_file | cut -d= -f2)" == "true" ]; then
  ftphost=$(grep ^ftphost $conf_file | cut -d= -f2)
  ftppath=$(grep ^ftppath $conf_file | cut -d= -f2)
  ftpuser=$(grep ^ftpuser $conf_file | cut -d= -f2)
  ftppass=$(grep ^ftppass $conf_file | cut -d= -f2)
  curl -s "ftp://${ftphost}/${ftppath}/" --upload-file "$bundle_name" --user "${ftpuser}:${ftppass}" --ftp-create-dirs
fi

if [ "$(grep save4web $conf_file | cut -d= -f2)" == "true" ]; then
  mv "$bundle_name" "/root/coredump.tgz"
else
  rm "$bundle_name"
fi

exit 0
