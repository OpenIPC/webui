#!/bin/sh

plugin="network"
source /usr/sbin/common-plugins

# $(date) $network_mode $network_interface $network_address
TEMPLATE_COMMON="# created at %s
auto %s
iface %s inet %s
"

TEMPLATE_MAC="    hwaddress ether \$(fw_printenv -n ethaddr || echo 00:00:23:34:45:66)\n"

# $network_address $network_netmask
TEMPLATE_STATIC="    # static address
    address %s
    netmask %s
"

# $network_ssid $network_password
TEMPLATE_WIRELESS="    post-up wpa_passphrase \"\$(fw_printenv -n wlanssid || echo %s)\" \"\$(fw_printenv -n wlanpass || echo %s)\" > /tmp/wpa_supplicant.conf
    post-up sed -i '2i \\\\\\\tscan_ssid=1' /tmp/wpa_supplicant.conf
    post-up wpa_supplicant -D nl80211,wext -i wlan0 -c /tmp/wpa_supplicant.conf -B
    post-down killall -q wpa_supplicant
"

# ppp_gpio=61
# $ppp_gpio $ppp_gpio $ppp_gpio $ppp_gpio $ppp_gpio
TEMPLATE_PPP="    # PPP
    pre-up echo %s > /sys/class/gpio/export
    pre-up echo out > /sys/class/gpio/gpio%s/direction
    pre-up echo 0 > /sys/class/gpio/gpio%s/value
    pre-up sleep 7
    post-down echo 1 > /sys/class/gpio/gpio%s/value
    post-down echo %s > /sys/class/gpio/unexport
"

# usb_vendor=0x2c7c; usb_product=0x6026
# $usb_vendor $usb_product
TEMPLATE_USB="    # USB
    pre-up echo 9 > /sys/class/gpio/export
    pre-up echo out > /sys/class/gpio/gpio9/direction
    pre-up echo 0 > /sys/class/gpio/gpio9/value
    pre-up modprobe usbserial vendor=%s product=%s
    pre-up modprobe rndis_host
    pre-up sleep 10
    post-down echo 1 > /sys/class/gpio/gpio9/value
    post-down echo 9 > /sys/class/gpio/unexport
"

# network_interface=wg0
# $network_interface $network_interface $network_interface
TEMPLATE_WIREGUARD="    # WireGuard
    # +static
    pre-up modprobe wireguard
    pre-up ip link add dev %s type wireguard
    pre-up wg setconf %s /etc/wireguard.conf
    post-down ip link del dev %s
"

show_help() {
  echo "Usage: $0 [OPTIONS]
Where:
  -i iface       Network interface.
  -m mode        Mode [dhcp, static].
  -h name        Hostname.

For wireless interface:
  -s SSID        WiFi network SSID.
  -p password    WiFi passphrase.

For static mode:
  -a address     Interface IP address.
  -n netmask     Network mask.
  -g address     Gateway IP address.
  -d addresses   DNS servers addresses.

  -v             Verbose output.
"
  exit 0
}

## override config values with command line arguments
while getopts a:d:D:g:h:i:k:m:n:p:s:t:v flag; do
	case ${flag} in
	a) network_address=${OPTARG} ;;
	d) network_nameservers=${OPTARG} ;;
	g) network_gateway=${OPTARG} ;;
	h) network_hostname=${OPTARG} ;;
	i) network_interface=${OPTARG} ;;
	n) network_netmask=${OPTARG} ;;
	m) network_mode=${OPTARG} ;;
	p) network_password=${OPTARG} ;;
	s) network_ssid=${OPTARG} ;;
	v) verbose=1 ;;
	esac
done

if [ $# -eq 0 ]; then
	show_help
	exit 1
fi

# shift dns2 to dns1 if dns1 if empty
#if [ -z "$network_dns_1" ]; then
#  network_dns_1="$network_dns_2"
#  network_dns_2=""
#fi
# set dns1 to localhost if none provided
# [ -z "$network_dns_1" ] && network_dns_1="127.0.0.1"

## validate mandatory values
[ -z "$network_interface" ] && echo "Network interface is not set" && exit 11

if [ "wlan0" = "$network_interface" ]; then
	[ -z "$network_ssid" ] && echo "Wireless network SSID is not set" && exit 12
	[ -z "$network_password" ] && echo "Wireless network passphrase is not set" && exit 13
fi

[ -z "$network_mode" ] && echo "Network mode is not set" && exit 14
if [ "static" = "$network_mode" ]; then
	[ -z "$network_address" ] && echo "Interface IP address is not set" && exit 15
	[ -z "$network_netmask" ] && echo "Netmask is not set" && exit 16
	#[ -z "$network_gateway" ] && echo "Gateway IP address is not set" && exit 17
	#[ -z "$network_dns_1" ] && echo "DNS1 IP address is not set" && exit 18
	#[ -z "$network_dns_2" ] && echo "DNS2 IP address is not set" && exit 19
fi

tmp_file=/tmp/${plugin}.conf
:>$tmp_file

#cat /etc/network/interfaces | sed "/^auto ${network_interface}\$/,/^\$/d" | sed -e :a -e '/^\n*$/{$d;N;};/\n$/ba' >$tmp_file

printf "$TEMPLATE_COMMON" "$(date)" $network_interface $network_interface $network_mode >>$tmp_file

if [ "eth0" = "$network_interface" ]; then
	printf "$TEMPLATE_MAC" >>$tmp_file
fi

if [ "static" = "$network_mode" ]; then
	printf "$TEMPLATE_STATIC" $network_address $network_netmask >>$tmp_file

	# skip gateway if empty
	if [ -n "$network_gateway" ]; then
		echo "    gateway ${network_gateway}" >>$tmp_file
	fi

	# skip dns servers if empty
	if [ -n "$network_nameservers" ]; then
		echo -n "    pre-up echo -e \"" >>$tmp_file
		for dns in ${network_nameservers//,/ }; do
			echo -n "nameserver ${dns}\n" >>$tmp_file
		done; unset dns
		echo "\" >/tmp/resolv.conf" >>$tmp_file
	fi
fi

if [ "wlan0" = "$network_interface" ]; then
	printf "$TEMPLATE_WIRELESS" $network_ssid $network_password >>$tmp_file
fi

# TODO: preset ppp_gpio
if [ "ppp0" = "$network_interface" ]; then
	printf "$TEMPLATE_PPP" $ppp_gpio $ppp_gpio $ppp_gpio $ppp_gpio $ppp_gpio >>$tmp_file
fi

# TODO: preset usb_vendor usb_product
if [ "usb0" = "$network_interface" ]; then
	printf "$TEMPLATE_USB" $usb_vendor $usb_product >>$tmp_file
fi

if [ "wg0" = "$network_interface" ]; then
	printf "$TEMPLATE_WIREGUARD" $network_interface $network_interface $network_interface >>$tmp_file
fi

mv $tmp_file /etc/network/interfaces.d/$network_interface

cat /etc/network/interfaces.d/$network_interface

exit

if [ -n "$network_hostname" ]; then
	_old_hostname="$(hostname)"
	if [ "$network_hostname" != "$_old_hostname" ]; then
		echo "$network_hostname" >/etc/hostname
		hostname "$network_hostname"
		sed -r -i "/127.0.1.1/s/(\b)${_old_hostname}(\b)/\1${network_hostname}\2/" /etc/hosts >&2
		killall udhcpc
		# page does not redirect without >/dev/null
		udhcpc -x hostname:$network_hostname -T 1 -t 5 -R -b -O search >/dev/null
	fi
fi

update_caminfo
generate_signature
touch /tmp/network-restart.txt

exit 0
