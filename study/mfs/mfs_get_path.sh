#!/bin/bash
#
# get file path via inode from MFS meta dump file.
# !!!! it's beta, use your own risk !!!!
# Version 0.1 /2010-02-05 release by timothy.lee/   
# Version 0.2 /2010-02-06 release by timothy.lee/ fix wrong child id in function getCP().
# Version 0.2.1 /2010-02-06 release by timothy.lee/ fix dead loop in main program.
#


### custom variables
meta_dump=$1
file_id=$2
mfs_mount_point=$3

### functions
USEAGE(){
	echo "Useage: $(basename $0) {META-DUMP-FILE} {FILE-INODE} [MFS-MOUNT-POINT]" 
	exit 0
}

getCP(){
	type=$1
	c_=$(grep -i " $3|n:" $2)
	p_=$(echo $c_ | awk '{print $2}' | cut -d '|' -f1 | xargs -i grep -i {}'|n:' $2)
	if [ "$type" == 'C' ]; then
		echo $c_
	elif [ "$type" == 'P' ]; then
		echo $p_
	else
		echo ''
	fi
}

getCPid(){
	type=$1
	c_id=$(echo "$4" | cut -d '|' -f1)
	p_id=$(echo "$3" | cut -d '|' -f1)
        if [ "$type" == 'C' ]; then
                echo $c_id
        elif [ "$type" == 'P' ]; then
                echo $p_id
        else
                echo ''
        fi
}

getIDname(){
	id_name=$(echo "$3" | cut -d ':' -f2)
	echo $id_name
}


### main
if [ ! -f "$meta_dump" ] || [ -z "file_id" ]; then
	USEAGE
fi

test -z "$mfs_mount_point" && mfs_mount_point='/MFS-MOUNT-POINT'

is_root=0
while [ "$is_root" != '1' ];
do
	this_c=$(getCP C $meta_dump $file_id)
	test -z "$this_c" && echo "INODE not found !" && exit 0
	this_p=$(getCP P $meta_dump $file_id)
	this_path=$(getIDname $this_c) 
	this_p_path=$(getIDname $this_p) 
	this_p_id=$(getCPid P $this_c); 
	if [ -z "$this_full_path" ]; then
		this_full_path="$this_path"
	else
		this_full_path="$this_path"/"$this_full_path"
	fi
	if [ "$this_p_id" != '1' ]; then
		file_id=$(getCPid P $this_c) 
		is_root=0
	else
		echo "$mfs_mount_point"/$this_full_path
		is_root=1
	fi
	#exit 0
done
