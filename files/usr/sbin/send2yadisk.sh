#!/bin/sh

config_file="/etc/yadisk.cfg"
curl_timeout=100

if [ ! -f "$config_file" ]; then
  echo -e "Error: ${config_file} not found."
  exit 1
fi

# read variables from config
eval $(grep = $config_file)

# exit if plugin is not enabled
# [ "$yadisk_enabled" != "true" ] && exit 0

webdav_mkdir()  {
  url="${url}/${1}"
  echo "curl $curl_options --request MKCOL $url"
  curl $curl_options --request MKCOL "$url"
}

webdav_upload() {
  url="${url}/$(TZ=$(cat /etc/TZ) date +"%G%m%d-%H%M%S").jpg"
  echo "curl $curl_options --upload-file $1 $url"
  curl $curl_options --request PUT --upload-file "$1" "$url"
}

url="https://webdav.yandex.ru"
tmp_file=/tmp/snap.jpg

# curl_options="--insecure --connect-timeout ${curl_timeout} --max-time ${curl_timeout}" # --silent

# get image from camera
curl $curl_options "http://127.0.0.1/image.jpg" --output "$tmp_file" --silent

# Yandex Disk user's credentials
curl_options="${curl_options} --user ${yadisk_login}:${yadisk_password}"
# SOCK5 proxy, if needed
if [ "$socks5_enabled" = "1" ]; then
  curl_options="${curl_options} --socks5-hostname ${yadisk_socks5_server}:${yadisk_socks5_port} --proxy-user ${yadisk_socks5_login}:${yadisk_socks5_password}"
fi

# create path to destication directory
subdirs="${yadisk_path// /_}"
subdirs="$(echo "$yadisk_path" | sed "s/$/\//")"
while [ -n "$subdirs" ]; do
  subdir="${subdirs%%/*}"
  [ -n "$subdir" ] && webdav_mkdir "$subdir"
  subdirs="${subdirs#*/}"
done

# save file
webdav_upload "$tmp_file"

exit 0
