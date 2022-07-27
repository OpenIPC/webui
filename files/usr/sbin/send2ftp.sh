#!/bin/sh

plugin="ftp"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

if [ ! -f "$config_file" ]; then
  echo "Error: ${config_file} not found."
  exit 1
fi

# read variables from config
[ -f "$config_file" ] && source $config_file

if [ "true" != "$ftp_enabled" ]; then
  echo "Sending to FTP is not enabled."
  exit 10
fi

# validate mandatory values
[ -z "$ftp_host" ] && echo -e "FTP host not found in config" && exit 11
[ -z "$ftp_port" ] && echo -e "FTP port not found in config" && exit 12

curl_options="--verbose --silent --connect-timeout ${curl_timeout} --max-time ${curl_timeout}" # --insecure

# FTP credentials, if given
if [ -n "$ftp_login" ] && [ -n "$ftp_password" ]; then
  curl_options="${curl_options} --user ${ftp_login}:${ftp_password}"
fi

# SOCK5 proxy, if needed
if [ "true" = "$ftp_socks5_enabled" ]; then
  source /etc/webui/socks5.conf
  curl_options="${curl_options} --socks5-hostname ${socks5_host}:${socks5_port} --proxy-user ${socks5_login}:${socks5_password}"
fi

url="ftp://${ftp_host}"
[ -n "$ftp_path" ] && url="${url}/${ftp_path// /%20}"
url="${url}/$(date +"$ftp_template")"

snapshot="/tmp/${plugin}_snap.jpg"

# get image from camera
curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
if [ $? -eq 0 ]; then
  curl ${curl_options} \
    --url ${url} \
    --upload-file ${snapshot} \
    --ftp-create-dirs >/tmp/webui/${plugin}.log 2>&1
  rm -f ${snapshot}
else
  echo "Cannot get a snapshot."
  exit 2
fi

exit 0
