#! /bin/bash

sudo su
mkdir /home/ubuntu/bucket

access_key="AKIAZDSHKL5YZFBH4PVT"
secret_access_key="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"
region="ap-south-1"
bucket_name="hithesh24r-001"
mount_path="/home/ubuntu/bucket"

aws configure set default.region $region
aws configure set aws_access_key_id $access_key
aws configure set aws_secret_access_key $secret_access_key

aws s3 sync $mount_path s3://$bucket_name
echo $access_key:$secret_access_key > "$HOME/.passwd_s3fs"
chmod 600 "$HOME/.passwd_s3fs"
s3fs $bucket_name $mount_path -o passwd_file="${HOME}/.passwd_s3fs",nonempty,allow_other,mp_umask=002,uid=1000,gid=1000 -o url=http://s3.$region.amazonaws.com,endpoint=$region,use_path_request_style
echo $bucket_name $mount_path fuse.s3fs _netdev,allow_other 0 0 >> "/etc/fstab"

cp /home/ubuntu/bucket/ssh_key.pub /home/ubuntu/.ssh/authorized_keys
