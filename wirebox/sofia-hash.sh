#!/bin/sh

MD5=$(echo -n "$@" | md5sum | awk '{print $1}')
i=0
while [ $i -le 7 ]; do
  n=`expr $(($((0x${MD5:$((2*$i*2)):2}))+$((0x${MD5:$((2*$i*2+2)):2})))) % $((0x3e))`
  if [ $n -gt 9 ]; then
    if [ $n -gt 35 ]; then
      n=$(($n + 61))
    else
      n=$(($n + 55))
    fi
  else
    n=$(($n + 0x30))
  fi
  printf "\x$(printf %x $n)"
  i=$(($i+1))
done
echo ""
