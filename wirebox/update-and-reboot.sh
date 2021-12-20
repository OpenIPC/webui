#!/bin/sh

lock_file=/tmp/webjob.lock

touch $lock_file

/root/longprocess.sh
# sysupgrade $1

rm $lock_file
#reboot