#!/bin/sh

echo_c() {
  # 31 red, 32 green, 33 yellow, 34 blue, 35 magenta, 36 cyan, 37 white, 38 grey
  [ -z "$HASERLVER" ] && t="\e[1;$1m$2\e[0m" || t="$2"
  echo -e "$t"
}

log_and_run() {
  echo_c 36 "$1"
  eval "$1"
}

clean_quit() {
  echo_c 37 "$2" >&2
  [ -f "$tmp_file" ] && rm $v_opts $tmp_file
  exit $1
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
  v) verbose=1
    v_opts="-v"
    ;;
  h) print_usage ;;
  esac
done

# validation
if [ -z "$branch" ]; then
  echo_c 33 "Mandatory parameter branch is not set!"
  print_usage
  exit 0
fi

etag_file=/root/.ui.etag
tmp_file="$(mktemp -u)"
cmd="curl --silent --location --insecure --fail"
[ "1" = "$verbose" ] && cmd="${cmd} --verbose"
cmd="${cmd} --etag-save ${etag_file}"
[ "1" != "$enforce" ] && [ -f "$etag_file" ] && cmd="${cmd} --etag-compare ${etag_file}"
cmd="${cmd} --url https://github.com/OpenIPC/microbe-web/archive/refs/heads/${branch}.zip"
cmd="${cmd} --output $tmp_file"
log_and_run "$cmd"
[ ! -f "$tmp_file" ] && clean_quit 1 "GitHub version matches the installed one. Nothing to update."

commit=$(tail -c 40 $tmp_file | cut -b1-7)
# date in ISO format. ugly but it works
_ts=$(unzip -l $tmp_file | head -5 | tail -1 | xargs | cut -d" " -f2)
timestamp="$(echo $_ts | cut -d- -f3)-$(echo $_ts | cut -d- -f1)-$(echo $_ts | cut -d- -f2)"

unzip_dir="/tmp/microbe-web-${branch}"
[ -d "$unzip_dir" ] && rm -rf $unzip_dir

cmd="unzip -o -d /tmp $tmp_file"
[ "1" = "$verbose" ] && cmd="${cmd} -q"
cmd="${cmd} -x microbe-web-dev/README.md microbe-web-dev/LICENSE microbe-web-dev/.git* microbe-web-dev/dev/* microbe-web-dev/docs/*"
log_and_run "$cmd"
upd_dir="${unzip_dir}/files"

echo_c 37 "Copy newer files to web directory"
for upd_file in $(find $upd_dir -type f -or -type l); do
  ovl_file=${upd_file#/tmp/microbe-web-${branch}/files}
  # echo "Overlay file ${ovl_file}"
  if [ ! -f "$ovl_file" ] || [ "$(diff -q $ovl_file $upd_file)" ]; then
    [ ! -d "${ovl_file%/*}" ] && mkdir -p $(dirname $ovl_file)
    cp $v_opts -f $upd_file $ovl_file
  fi
done

echo_c 37 "Remove absent files from overlay"
for file in $(diff -qr "/var/www" "${upd_dir}/var/www" | grep "Only in /var/www:" | cut -d':' -f2 | tr -d "^ "); do
  [ "$file" != "$etag_file" ] && rm $v_opts -f /var/www/${file}
  mount -o remount /
done

echo_c 37 "Delete bundle"
rm $v_opts -f $tmp_file

echo_c 37 "Delete temp directory"
rm $v_opts -rf /tmp/microbe-web-${branch}

if [ -n "$error" ]; then
  rm $v_opts $etag_file
  clean_quit 2 "ATTENTION! There were errors!"
fi

echo "${branch}+${commit}, ${timestamp}" >/var/www/.version
[ -f /tmp/sysinfo.txt ] && rm $v_opts /tmp/sysinfo.txt
clean_quit 0 "Done."
