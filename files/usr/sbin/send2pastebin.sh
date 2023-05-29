#!/bin/sh

if [ -z "$1" ]; then
	echo "Usage: $0 <filename>"
	exit 1
fi

file=$1
[ ! -f $file ] && echo "Cannot find file $file" && exit 2
[ -z "$(cat $file)" ] && echo "File $file is empty" && exit 3

url=$(cat $file | nc termbin.com 9999)
echo $url
exit 0
