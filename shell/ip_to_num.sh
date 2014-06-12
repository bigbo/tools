#!/bin/bash
#
NUM2IP () {
echo  |awk -v IPNUM=$1 '{ for (I = 4 ; I >=1; I-- ){
  printf (IPNUM % (256^I)- (IPNUM % 256^(I-1)))/256^(I-1)
  if (I >1 ) printf "."
}
printf "\n"
}'
}
IP2NUM () {
echo $1 |awk  'BEGIN{NUM=0 ; FS="."}{for (I = NF ; I >=1; I-- )
 NUM=$I*256^(NF-I)+NUM
 print NF
}END{printf "%d\n",NUM}'
}
if [ $# -ne 2 ] ;then
echo "Usage: $0 -c ip_address or $0 -r num2convert"
exit 1
fi
if [ $1 = "-c" ] ; then
IP2NUM $2
elif [ $1 = "-r" ] ; then
NUM2IP $2
fi
