#!/bin/sh

plugin="openwall"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

log_file=/tmp/webui/${plugin}.log
mkdir -p $(dirname $log_file)
:>$log_file

[ "false" = "$openwall_enabled" ] &&
  echo "Sending to OpenIPC Wall is disabled." && exit 10

snapshot4cron.sh
[ $? -ne 0 ] && echo "Cannot get a snapshot" && exit 2
snapshot=/tmp/snapshot4cron.jpg
[ ! -f "$snapshot" ] && echo "Cannot find a snapshot" && exit 3

flash_size=$(awk '{sum+=sprintf("0x%s", $2);} END{print sum/1048576;}' /proc/mtd)
fw_variant=$(grep "BUILD_OPTION" /etc/os-release | cut -d= -f2 | tr -d /\"/); [ -z "$fw_variant" ] && fw_variant="lite"
fw_version=$(grep "OPENIPC_VERSION" /etc/os-release | cut -d= -f2 | tr -d /\"/)
network_hostname=$(hostname -s)
network_macaddr=$(ifconfig -a | grep HWaddr | sed s/.*HWaddr// | sed "s/ //g" | uniq | tail -1)
sensor=$(ipcinfo --short-sensor)
soc=$(ipcinfo --chip-name)
soc_temperature=$(ipcinfo --temp)
uptime=$(uptime | sed -r 's/^.+ up ([^,]+), .+$/\1/')

# validate mandatory values
[ ! -f "$snapshot" ] &&
  echo "Snapshot file not found" && exit 11
[ -z "$network_macaddr" ] &&
  echo "MAC address not found" && exit 12

command="curl --verbose" # --silent --insecure
command="${command} --connect-timeout ${curl_timeout}"
command="${command} --max-time ${curl_timeout}"

# SOCK5 proxy, if needed
if [ "true" = "$yadisk_socks5_enabled" ]; then
  source /etc/webui/socks5.conf
  command="${command} --socks5-hostname ${socks5_host}:${socks5_port}"
  command="${command} --proxy-user ${socks5_login}:${socks5_password}"
fi

command="${command} --url https://openipc.org/snapshots"
command="${command} -F 'mac_address=${network_macaddr}'"
command="${command} -F 'firmware=${fw_version}-${fw_variant}'"
command="${command} -F 'flash_size=${flash_size}'"
command="${command} -F 'hostname=${network_hostname}'"
command="${command} -F 'sensor=${sensor}'"
command="${command} -F 'soc=${soc}'"
command="${command} -F 'soc_temperature=${soc_temperature}'"
command="${command} -F 'uptime=${uptime}'"
command="${command} -F 'file=@${snapshot}'"

echo "$command" >>$log_file
eval "$command" >>$log_file 2>&1
cat $log_file

exit 0
