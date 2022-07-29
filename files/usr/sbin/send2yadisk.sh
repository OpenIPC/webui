#!/bin/sh

plugin="yadisk"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

log_file=/tmp/webui/${plugin}.log
mkdir -p $(dirname $log_file)
:>$log_file

show_help() {
  echo "Usage: $0 [-u username] [-P password] [-h]
  -d path     Directory on server.
  -f file     File to upload.
  -u username Yandex Disk username.
  -P password Yandex Disk username.
  -h          Show this help.
"
  exit 0
}

# read variables from config
[ -f "$config_file" ] && source $config_file

# override config values with command line arguments
while getopts d:f:P:u:h flag; do
  case ${flag} in
  d) yadisk_path=${OPTARG} ;;
  f) yadisk_file=${OPTARG} ;;
  P) yadisk_password=${OPTARG} ;;
  u) yadisk_username=${OPTARG} ;;
  h) show_help ;;
  esac
done

[ "false" = "$yadisk_enabled" ] &&
  echo "Sending to Yandex Disk is disabled." && exit 10


if [ -z "$yadisk_file" ]; then
  snapshot="/tmp/${plugin}_snap.jpg"
  curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
  [ $? -ne 0 ] && echo "Cannot get a snapshot" && exit 2
  yadisk_file=$snapshot
fi

webdav_mkdir() {
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
  unset cmd
  unset result
}

# validate mandatory values
[ -z "$yadisk_username" ] &&
  echo "Yandex Disk username not found" && exit 11
[ -z "$yadisk_password" ] &&
  echo "Yandex Disk password not found" && exit 12

command="curl --verbose" # --silent --insecure
command="${command} --connect-timeout ${curl_timeout}"
command="${command} --max-time ${curl_timeout}"

# Yandex Disk credentials
command="${command} --user '${yadisk_username}:${yadisk_password}'"

# SOCK5 proxy, if needed
if [ "true" = "$yadisk_socks5_enabled" ]; then
  source /etc/webui/socks5.conf
  command="${command} --socks5-hostname ${socks5_host}:${socks5_port}"
  command="${command} --proxy-user ${socks5_login}:${socks5_password}"
fi

# create path to destination directory
url="https://webdav.yandex.ru"
subdirs="${yadisk_path// /_}" # prevent splitting by whitespaces
subdirs="$(echo "$yadisk_path" | sed "s/[^\/]$/\//")" # add final slash if missing
while [ -n "$subdirs" ]; do
  subdir="${subdirs%%/*}"
  subdir="${subdir// /%20}" # convert each space into %20
  if [ -n "$subdir" ]; then
    url="${url}/${subdir}"
    _command="${command} --request MKCOL ${url}" # disposable subcommand
    echo "$_command" >>$log_file
    eval "$_command" >>$log_file 2>&1
  fi
  subdirs="${subdirs#*/}"
done

# upload file
url="${url}/$(TZ=$(cat /etc/TZ) date +"%G%m%d-%H%M%S").jpg"
command="${command} --url ${url}"
command="${command} --request PUT"
command="${command} --upload-file ${snapshot}"

echo "$command" >>$log_file
eval "$command" >>$log_file 2>&1
cat $log_file

[ -f ${snapshot} ] && rm -f ${snapshot}

exit 0
