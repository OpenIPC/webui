#!/bin/sh

echo_c() {
  [ -z "$HASERLVER" ] && t="\e[1;$1m$2\e[0m" || t="$2"
  echo -e "$t"
}

print_usage() {
  echo "
Usage: $0 -b <branch> [-f]

  -f, --force           install even if same version
  -h, --help            display this help and exit
"
}

args=""
while [ $# -gt "0" ]; do
  case "$1" in
    -b|--branch)
      branch="$2"
      shift
      shift
      ;;
    -f|--force)
      enforce=1
      shift
      ;;
    -h|--help)
      print_usage
      exit
      ;;
    -v|--verbose)
      verbose=1
      shift
      ;;
    -*|--*)
      echo_c 97 "\nUnknown option: $1"
      print_usage
      shift
      exit 1
      ;;
    *)
      args="${args} $1"
      shift
      ;;
  esac
done

if [ -z "$branch" ]; then
  echo_c 93 "Mandatory parameter branch is not set!"
  print_usage
  exit 0
fi

url="https://github.com/OpenIPC/microbe-web/archive/refs/heads/${branch}.zip"
tmp_file=/tmp/microbe-web.zip
etag_file=/root/.ui.etag
opts="--silent --location --insecure --etag-save ${etag_file}"
[ -n "$verbose" ] && [ "$verbose" -eq 1 ] && opts="${opts} --verbose"

if [ "$enforce" != "1" ]; then
  [ -f "$etag_file" ] && opts="${opts} --etag-compare ${etag_file}"
fi

curl $opts -o $tmp_file $url
if [ ! -f "$tmp_file" ]; then
  echo_c 97 "GitHub version matches the installed one. Nothing to update." >&2
  exit 1
fi

commit=$(tail -c 40 $tmp_file|cut -b1-7)
_ts=$(unzip -l $tmp_file|head -5|tail -1|xargs|cut -d" " -f2)
timestamp="$(echo $_ts|cut -d- -f3)-$(echo $_ts|cut -d- -f1)-$(echo $_ts|cut -d- -f2)" # ugly but it works

unzip_dir="/tmp/microbe-web-${branch}"
[ -d "$unzip_dir" ] && rm -rf $unzip_dir
unzip -o -d /tmp $tmp_file -x microbe-web-dev/README.md microbe-web-dev/.git* microbe-web-dev/LICENSE microbe-web-dev/docs/* microbe-web-dev/wirebox/*
upd_dir="${unzip_dir}/files"

echo_c 97 "Copy newer files to web directory"
for upd_file in $(find $upd_dir -type f -or -type l); do
  ovl_file=${upd_file#/tmp/microbe-web-${branch}/files}
  # echo "Overlay file ${ovl_file}"
  if [ ! -f "$ovl_file" ] || [ "$(diff -q $ovl_file $upd_file)" ]; then
    [ ! -d "${ovl_file%/*}" ] && mkdir -p $(dirname $ovl_file)
    cp -f $upd_file $ovl_file
  fi
done

echo_c 97 "Remove absent files from overlay"
for file in $(diff -qr "/var/www" "${upd_dir}/var/www" | grep "Only in /var/www:" | cut -d':' -f2 | tr -d "^ "); do
  [ "$file" != "$etag_file" ] && rm -f /var/www/${file}
  mount -oremount /
done

echo_c 97 "Delete bundle"
rm -f $tmp_file

echo_c 97 "Delete temp directory"
rm -fr /tmp/microbe-web-${branch}

if [ -z "$error" ]; then
  echo "${branch}+${commit}, ${timestamp}" > /var/www/.version
  exit 0
else
  rm $etag_file
  echo_c 91 "ATTENTION! There were errors!" >&2
  exit 2
fi
