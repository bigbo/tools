#!/bin/bash
#
# check file modify date from MFS meta dump file.
# !!!! it's beta, use your own risk !!!!
# Version 0.1 /2010-02-05 release by timothy.lee/   
# Version 0.2 /2010-02-08 release by timothy.lee/ add function mTimeCheck, rewrite main program.
#


### custom variables
meta_dump=$1
day_range=$2
output_file=$3

### functions
USEAGE(){
        echo "Useage: $(basename $0) {META-DUMP-FILE} {DAY-RANGE eg.-1day} {OUTPUT-FILE}" 
        exit 0
}

splitMETAdump(){
	part=$1
	ln=$(nl $2 | grep '# -------------------------------------------------------------------' | awk '{ print $1 }')
	start_ln=$(echo $ln | awk '{ print $'$part' }')
	part=$(($part+1))
	end_ln=$(echo $ln | awk '{ print $'$part' }')
	test -z $end_ln && end_ln=$(nl $2 | tail -n1 | awk '{ print $1}')
	sed -n "$start_ln","$end_ln"p $2 | grep -v '# -------------------------------------------------------------------'
}

mTimeCheck(){
	echo '- split'
	cat $1 | cut -d '|' -f1 > "$1".p1
	cat $1 | cut -d ':' -f 7 | cut -d ',' -f1 > "$1".p2
	echo '- merge'
	paste "$1".p2 "$1".p1 > "$1".paste
	echo "$date_y_sec @" >> "$1".paste
	echo '- sort'
	sort "$1".paste | nl -s 'line ' > "$1".sort
	s_ln=$(cat "$1".sort | grep "$date_y_sec" | awk '{ print $1 }' | cut -d 'l' -f1)
	e_ln=$(tail -n1 "$1".sort | awk '{ print $1 }' | cut -d 'l' -f 1)
	echo '- write'
	sed -n "$s_ln","$e_ln"p "$1".sort | awk '{ print $2" "$3}' > $2
	rm $1 $1.p1 $1.p2 $1.paste $1.sort
}

### main
if [ ! -f "$meta_dump" ] || [ -z "$output_file" ] ; then
	USEAGE
fi
test -z $day_range && day_range='-1day'

date_y="$(date -d $day_range +"%Y-%m-%d") 00:00:00"
date_y_sec=$(eval date -d \"$date_y\" +%s)

echo 'read dump file ...'
splitMETAdump 1 $1 | grep -v '^D|i' | awk '{ print $2$4 }' > "$output_file"."$$"
echo 'process dump file ...'
mTimeCheck "$output_file"."$$" "$output_file"
echo "done ! create log file $output_file success."

