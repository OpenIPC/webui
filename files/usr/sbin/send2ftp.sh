#!/bin/sh

plugin="ftp"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

if [ ! -f "$config_file" ]; then
  echo -e "Error: ${config_file} not found."
  exit 1
fi

# read variables from config
[ -f "$config_file" ] && source $config_file

snapshot="/tmp/ftp_snap.jpg"

# get image from camera
curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
if [ $? -eq 0 ]; then
  curl_options="--silent --insecure --connect-timeout ${curl_timeout} --max-time ${curl_timeout}"

  # FTP credentials
  curl_options="${curl_options} --user ${ftp_login}:${ftp_password}"

  # SOCK5 proxy, if needed
  if [ "true" = "$ftp_socks5_enabled" ]; then
    source /etc/webui/socks5.conf
    curl_options="${curl_options} --socks5-hostname ${socks5_server}:${socks5_port} --proxy-user ${socks5_login}:${socks5_password}"
  fi

  ftp_url="ftp://${ftp_host}"
  [ -n "$ftp_path" ] && ftp_url="${ftp_url}/${ftp_path}"
  ftp_url="${ftp_url}/$(date +"$ftp_template")"

  curl "$ftp_url" --upload-file "$snapshot" --ftp-create-dirs $curl_options
else
  echo "Cannot get a snapshot."
  exit 1
fi

exit 0
