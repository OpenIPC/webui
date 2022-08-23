#!/bin/sh

echo_c() {
  # 31 red, 32 green, 33 yellow, 34 blue, 35 magenta, 36 cyan, 37 white, 38 grey
  [ -z "$HASERLVER" ] && t="\e[1;$1m$2\e[0m" || t="$2"
  echo -e "$t"
}

print_usage() {
  echo "Usage: $0 -b <branch> [-v] [-f] [-h]
  -b <branch>  Git branch to use.
  -f           Install even if same version.
  -v           Verbose output.
  -h           Show this help.
"
  exit 0
}

# override config values with command line arguments
while getopts b:fvh flag; do
  case ${flag} in
  b) branch=${OPTARG} ;;
  f) enforce=1 ;;
  v) verbose=1 ;;
  h) print_usage ;;
  esac
done

if [ -z "$branch" ]; then
  echo_c 33 "Mandatory parameter branch is not set!"
  print_usage
  exit 0
fi

tmp_file=/tmp/microbe-web.zip
etag_file=/root/.ui.etag

# url to retrieve update from
url="https://github.com/OpenIPC/microbe-web/archive/refs/heads/${branch}.zip"
curl_opts="--location --insecure --etag-save ${etag_file}" #--silent

if [ "1" != "$enforce" ]; then
  [ -f "$etag_file" ] && curl_opts="${curl_opts} --etag-compare ${etag_file}"
fi

if [ "1" = "$verbose" ]; then
  curl_opts="${curl_opts} --verbose"
  unzip_opts=""
  cp_opts="-v"
  rm_opts="-v"
else
  curl_opts="${curl_opts} --silent"
  unzip_opts="-q"
  cp_opts=""
  rm_opts=""
fi

cmd="curl $curl_opts --output $tmp_file --url $url"
echo_c 36 "$cmd"
$cmd

if [ ! -f "$tmp_file" ]; then
  echo_c 37 "GitHub version matches the installed one. Nothing to update." >&2
  exit 1
fi

commit=$(tail -c 40 $tmp_file|cut -b1-7)
_ts=$(unzip -l $tmp_file|head -5|tail -1|xargs|cut -d" " -f2)
timestamp="$(echo $_ts|cut -d- -f3)-$(echo $_ts|cut -d- -f1)-$(echo $_ts|cut -d- -f2)" # ugly but it works

unzip_dir="/tmp/microbe-web-${branch}"
[ -d "$unzip_dir" ] && rm -rf $unzip_dir
unzip $unzip_opts -o -d /tmp $tmp_file -x microbe-web-dev/README.md microbe-web-dev/.git* microbe-web-dev/LICENSE microbe-web-dev/docs/* microbe-web-dev/wirebox/*
upd_dir="${unzip_dir}/files"

echo_c 37 "Copy newer files to web directory"
for upd_file in $(find $upd_dir -type f -or -type l); do
  ovl_file=${upd_file#/tmp/microbe-web-${branch}/files}
  # echo "Overlay file ${ovl_file}"
  if [ ! -f "$ovl_file" ] || [ "$(diff -q $ovl_file $upd_file)" ]; then
    [ ! -d "${ovl_file%/*}" ] && mkdir -p $(dirname $ovl_file)
    cp $cp_opts -f $upd_file $ovl_file
  fi
done

echo_c 37 "Remove absent files from overlay"
for file in $(diff -qr "/var/www" "${upd_dir}/var/www" | grep "Only in /var/www:" | cut -d':' -f2 | tr -d "^ "); do
  [ "$file" != "$etag_file" ] && rm $rm_opts -f /var/www/${file}
  mount -o remount /
done

echo_c 37 "Delete bundle"
rm $rm_opts -f $tmp_file

echo_c 37 "Delete temp directory"
rm $rm_opts -f -r /tmp/microbe-web-${branch}

if [ -z "$error" ]; then
  echo "${branch}+${commit}, ${timestamp}" >/var/www/.version
  [ -f /tmp/sysinfo.txt ] && rm $rm_opts /tmp/sysinfo.txt
  echo_c 37 "Done."
  exit 0
else
  rm $rm_opts $etag_file
  echo_c 31 "ATTENTION! There were errors!" >&2
  exit 2
fi
