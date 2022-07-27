#!/bin/sh

plugin="yadisk"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

mkdir -p /tmp/webui

if [ ! -f "$config_file" ]; then
  echo "Error: ${config_file} not found."
  exit 1
fi

# read variables from config
[ -f "$config_file" ] && source $config_file

if [ "true" != "$yadisk_enabled" ]; then
  echo "Sending to Yandex Disk is not enabled."
  exit 10
fi

webdav_mkdir()  {
  url="${url}/${1}"
  cmd="curl ${curl_options} --request MKCOL ${url}"
  echo "$cmd" >>/tmp/webui/${plugin}.log
  result="$($cmd 2>&1)"
  echo "$result" >>/tmp/webui/${plugin}.log
  if [ "${result:1:6}" = '"ok":f' ]; then
    echo "Cannot create folder at Yandex Disk."
    echo "$result"
    exit 3
  fi
  unset cmd; unset result
}

webdav_upload() {
  url="${url}/$(TZ=$(cat /etc/TZ) date +"%G%m%d-%H%M%S").jpg"
  cmd="curl ${curl_options} --request PUT --upload-file ${1} ${url}"
  echo "$cmd" >>/tmp/webui/${plugin}.log
  result="$($cmd 2>&1)"
  echo "$result" >>/tmp/webui/${plugin}.log
  if [ "${result:1:6}" = '"ok":f' ]; then
    echo "Cannot upload snapshot to Yandex Disk."
    echo "$result"
    exit 4
  fi
  unset cmd; unset result
}

# validate mandatory values
[ -z "$yadisk_login"    ] && echo -e "Yandex Disk login not found in config" && exit 11
[ -z "$yadisk_password" ] && echo -e "Yandex Disk password not found in config" && exit 12

curl_options="--verbose --silent --insecure --connect-timeout ${curl_timeout} --max-time ${curl_timeout}"

# Yandex Disk credentials
curl_options="${curl_options} --user ${yadisk_login}:${yadisk_password}"

# SOCK5 proxy, if needed
if [ "true" = "$yadisk_socks5_enabled" ]; then
  source /etc/webui/socks5.conf
  curl_options="${curl_options} --socks5-hostname ${socks5_host}:${socks5_port} --proxy-user ${socks5_login}:${socks5_password}"
fi

url="https://webdav.yandex.ru"

snapshot="/tmp/${plugin}_snap.jpg"

# get image from camera
curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
if [ $? -eq 0 ]; then
  :>/tmp/webui/${plugin}.log
  # create path to destination directory
  subdirs="${yadisk_path// /_}" # prevent splitting by whitespaces
  subdirs="$(echo "$yadisk_path" | sed "s/[^\/]$/\//")" # add final slash if missing
  while [ -n "$subdirs" ]; do
    subdir="${subdirs%%/*}"
    subdir="${subdir// /%20}" # convert each space to %20 for url
    [ -n "$subdir" ] && webdav_mkdir "${subdir}"
    subdirs="${subdirs#*/}"
  done

  # upload file
  webdav_upload "$snapshot"
  rm -f ${snapshot}
else
  echo "Cannot get a snapshot."
  exit 2
fi

exit 0
