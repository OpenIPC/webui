#!/bin/sh
PASSWORD="12345"
MD5_HASH=$(echo -n "${PASSWORD}" | md5sum | awk '{print $1}')
echo "PASSWORD: ${PASSWORD}"
echo "MD5 HASH: ${MD5_HASH}"
for i in {0..7};
do
	x=$(printf '%d' "'$(echo ${MD5_HASH:$((2*$i*2)):2} | xxd -r -p)")
	y=$(printf '%d' "'$(echo ${MD5_HASH:$((2*$i*2+2)):2} | xxd -r -p)")
	n=`expr $(($x+$y)) % $((0x3e))`

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
done

