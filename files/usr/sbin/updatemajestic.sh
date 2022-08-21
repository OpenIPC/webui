#!/bin/sh

check_flash_memory_size() {
  if [ $(awk '{sum+=sprintf("0x%s", $2);} END{print sum/1048576;}' /proc/mtd) -lt 16 ]; then
    echo "Flash memory size is less than 16MB. Aborting."
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
  mj_meta_file=/tmp/mj_meta.txt
  mj_meta_url=${mj_url//.bz2/.meta}

  echo "Retrieving update info from ${mj_url} ..."
  if [ "200" != $(curl --silent --url $mj_meta_url -f -w %{http_code} -o /dev/null) ]; then
    echo "Cannot retrieve ${mj_meta_url} file. Aborting."
    exit 2
  fi

  curl --silent --url $mj_meta_url -o $mj_meta_file
  mj_version_new=$(sed -n 1p $mj_meta_file)

  echo "Installed Majestic: $mj_version"
  echo "Available Majestic: $mj_version_new"

  if [ "$mj_version_new" = "$mj_version" ]; then
    echo "Same version. No update available."
    exit 3
  fi

  # NB! size in bytes, but since blocks are 1024 bytes each, we are safe here for now.
  # Rounding up by priming, since $(()) sucks at floats.
  mj_filesize_new=$(( ($(sed -n 2p $mj_meta_file) + 1024) / 1024 ))

  # space available for update
  # NB! sizes are in allocated blocks.
  free_space=$(df | grep /overlay | xargs | cut -d' ' -f4)
  available_space=$(( ${free_space:=0} + ${mj_filesize_ol:=0} - 1 ))
}

check_space() {
  if [ "$mj_filesize_new" -gt "$available_space" ]; then
    echo "Not enough space to update Majestic!"
    echo "Update requires ${mj_filesize_new}K, but only ${available_space}K is available."
    if [ "$mj_filesize_ol" -ge "1" ]; then
      echo "(${free_space}K of unallocated space plus ${mj_filesize_ol:=0}K Majestic in overlay)"
    fi
    exit 4
  fi
}

update_majectic() {
  echo "Updating Majestic ..."
  # remove Majestic from overlay
  [ -f "$mj_bin_file_ol" ] && rm $mj_bin_file_ol && mount -oremount /
  # install new version
  curl --silent --insecure --location -o - --url $mj_url | bunzip2 | tar -x ./majestic -C /usr/bin/
  if [ $? -ne 0 ]; then
    echo "Cannot retrieve update from server."
    exit 5
  fi
}

check_flash_memory_size

get_system_info
check_space
update_majectic

echo "Done. Majestic $($mj_bin_file -v) installed in overlay."
echo "Unconditional reboot"
reboot
