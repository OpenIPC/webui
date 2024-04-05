#!/bin/sh
url="https://github.com/openipc/webui/archive/refs/heads/master.zip"

tmp_zip=$(mktemp -u)
curl -s -L $url -o $tmp_zip

tmp_dir=$(mktemp -d)
unzip -q -o -d $tmp_dir $tmp_zip

repo=$(ls $tmp_dir)
rm -f $(find /var/www -type f)

echo "Copy files to web directory"
cp -rf $tmp_dir/$repo/files/* /

echo "Delete temporary files"
rm -rf $tmp_dir $tmp_zip
