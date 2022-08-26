#!/bin/sh

show_help() {
  echo "Usage: $0 [OPTIONS]
  -m          Reset Majestic config.
  -h          Show this help.
"
  exit 0
}

reset_majestic() {
  cp -f /rom/etc/majestic.yaml /etc/majestic.yaml
}

while getopts hm flag; do
  case ${flag} in
  m) reset_majestic ;;
  h) show_help ;;
  esac
done

exit 0
