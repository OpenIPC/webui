#!/bin/sh

config_file="/etc/yadisk.cfg"
curl_timeout=100

if [ ! -f "$config_file" ]; then
  echo -e "Error: ${config_file} not found."
  exit 1
fi

# read variables from config
source $config_file

# exit if plugin is not enabled
# [ "$yadisk_enabled" != "true" ] && exit 0

webdav_mkdir()  {
  url="${url}/${1}"
  result=$(curl $curl_options --request MKCOL "$url")
  if [ "${result:1:6}" = '"ok":f' ]; then
    echo "Cannot create folder at Yandex Disk."
    echo $result
    exit 1
  fi
}

webdav_upload() {
  url="${url}/$(TZ=$(cat /etc/TZ) date +"%G%m%d-%H%M%S").jpg"
  result=$(curl $curl_options --request PUT --upload-file "$1" "$url")
  if [ "${result:1:6}" = '"ok":f' ]; then
    echo "Cannot upload snapshot to Yandex Disk."
    echo $result
    exit 1
  fi
}

url="https://webdav.yandex.ru"
snapshot="/tmp/yadisk_snap.jpg"

# get image from camera
curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
if [ $? -eq 0 ]; then
  curl_options="--silent --insecure --connect-timeout ${curl_timeout} --max-time ${curl_timeout}"

  # Yandex Disk user's credentials
  curl_options="${curl_options} --user ${yadisk_login}:${yadisk_password}"

  # SOCK5 proxy, if needed
  if [ "true" = "$yadisk_socks5_enabled" ]; then
    source /etc/webui/socks5.conf
    curl_options="${curl_options} --socks5-hostname ${socks5_server}:${socks5_port} --proxy-user ${socks5_login}:${socks5_password}"
  fi

  # create path to destination directory
  subdirs="${yadisk_path// /_}"
  subdirs="$(echo "$yadisk_path" | sed "s/$/\//")"
  while [ -n "$subdirs" ]; do
    subdir="${subdirs%%/*}"
    [ -n "$subdir" ] && webdav_mkdir "$subdir"
    subdirs="${subdirs#*/}"
  done
  # upload file
  webdav_upload "$snapshot"
else
  echo "Cannot get a snapshot."
  exit 1
fi

exit 0
