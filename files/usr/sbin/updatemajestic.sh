#!/bin/sh

source /usr/sbin/common

clean_quit() {
	[ -f "$mj_meta_file" ] && rm $mj_meta_file
	exit $1
}

print_usage() {
	echo "Usage: $0 [-v] [-f] [-h]
  -f           Install even if same version.
  -v           Verbose output.
  -h           Show this help.
"
	exit 0
}

# default
curl_opts="--silent --insecure --location --fail" # --write-out %{http_code}

# override config values with command line arguments
while getopts b:fvh flag; do
	case ${flag} in
	b) branch=${OPTARG} ;;
	f) enforce=1 ;;
	v) verbose=1
		curl_opts="${curl_opts} --verbose"
		v_opts="-v"
		;;
	h) print_usage ;;
  esac
done

check_flash_memory_size() {
	if [ $(awk '{sum+=sprintf("0x%s", $2);} END{print sum/1048576;}' /proc/mtd) -lt 16 ]; then
		echo_c 31 "Flash memory is smaller than 16MB. Aborting."
		exit 1
  fi
}

get_system_info() {
	# system
	fw_build=$(grep "GITHUB_VERSION" /etc/os-release | cut -d= -f2 | tr -d /\"/)
	fw_variant=$(grep "BUILD_OPTION" /etc/os-release | cut -d= -f2 | tr -d /\"/)
	fw_version=$(grep "OPENIPC_VERSION" /etc/os-release | cut -d= -f2 | tr -d /\"/)
	overlay_root=$(mount | grep upperdir= | sed -r 's/^.*upperdir=([a-z\/]+).+$/\1/')
	soc=$(ipcinfo --chip-name)
	soc_family=$(ipcinfo --family)
	soc_vendor=$(ipcinfo --vendor)

	# majestic
	mj_bin_file=/usr/bin/majestic
	mj_url="http://openipc.s3-eu-west-1.amazonaws.com/majestic.${soc_family}.${fw_variant:-lite}.master.tar.bz2"
	mj_version=$($mj_bin_file -v)

	# majestic in firmware
	mj_filesize_fw=$(ls -s $mj_bin_file | xargs | cut -d' ' -f1)

	# majestic in overlay
	mj_bin_file_ol="${overlay_root}${mj_bin_file}"
	[ -f "$mj_bin_file_ol" ] && mj_filesize_ol=$(ls -s $mj_bin_file_ol | xargs | cut -d' ' -f1)

	# majestic online
	#mj_meta_file=/tmp/mj_meta.txt
	mj_meta_file=$(mktemp)
	mj_meta_url=${mj_url//.bz2/.meta}

	echo_c 37 "Retrieving update info"
	echo_c 38 "from ${mj_meta_url}"
	log_and_run "curl $curl_opts --url $mj_meta_url --output $mj_meta_file"
	if [ $? -ne 0 ]; then
		echo_c 31 "Cannot retrieve ${mj_meta_url} file. Aborting."
		clean_quit 2
	fi

	echo_c 37 "\nComparing versions"
	mj_version_new=$(sed -n 1p $mj_meta_file)
	echo_c 38 "Installed: $mj_version\nAvailable: $mj_version_new\n"
	if [ "$mj_version_new" = "$mj_version" ]; then
		echo_c 32 "Update is the same version!"
		if [ "1" = "$enforce" ]; then
			echo_c 33 "Enforced re-installation."
		else
			echo_c 37 "Nothing to update. Quitting..."
			clean_quit 3
		fi
	fi
	echo
}

check_space() {
	# NB! size in bytes, but since blocks are 1024 bytes each, we are safe here for now.
	# Rounding up by priming, since $(()) sucks at floats.
	mj_filesize_new=$(( ($(sed -n 2p $mj_meta_file) + 1024) / 1024 ))

	# space available for update
	# NB! sizes are in allocated blocks.
	free_space=$(df | grep /overlay | xargs | cut -d' ' -f4)
	available_space=$(( ${free_space:=0} + ${mj_filesize_ol:=0} - 1 ))

	if [ "$mj_filesize_new" -gt "$available_space" ]; then
		echo_c 31 "Not enough space to update Majestic!"
		echo_c 37 "Update requires ${mj_filesize_new}K, but only ${available_space}K is available."
		if [ "$mj_filesize_ol" -ge "1" ]; then
			echo_c 37 "(${free_space}K of unallocated space plus ${mj_filesize_ol:=0}K Majestic in overlay)"
		fi
		clean_quit 4
	fi
}

update_majectic() {
	echo_c 37 "Updating Majestic"
	echo_c 38 "from ${mj_url}"

	echo_c 35 "Killing Majestic process"
	log_and_run "killall majestic"
	sleep 2

	# remove Majestic from overlay
	if [ -f "$mj_bin_file_ol" ]; then
		echo_c 37 "Deleting existing Majestic from overlay"
		log_and_run "rm $mj_bin_file_ol && mount -o remount /"
	fi

	# retrieve new version
	log_and_run "curl $curl_opts --url $mj_url --output - | bunzip2 | tar x $v_opts ./majestic -C /tmp/"
	if [ $? -ne 0 ]; then
		echo_c 31 "Cannot retrieve update from server."
		clean_quit 5
	fi

	# install new version
	log_and_run "mv /tmp/majestic $mj_bin_file"
	if [ $? -ne 0 ]; then
		echo_c 31 "Cannot replace $mj_bin_file."
		clean_quit 6
	fi
}

echo_c 37 "Majestic Updater\n"

check_flash_memory_size

get_system_info
check_space
update_majectic

echo_c 37 "Done."
echo_c 32 "Majestic $($mj_bin_file -v) installed in overlay.\n"
echo_c 37 "Unconditional reboot"
umount -a -t nfs -l
reboot -f
