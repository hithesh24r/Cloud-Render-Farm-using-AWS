#! /bin/bash

sudo su
mkdir /home/ubuntu/bucket
touch /etc/ansible/playbook.yaml
touch /etc/ansible/ansible.cfg
touch /etc/ansible/hosts

cd /home/ubuntu
ssh-keygen -t rsa -N "" -f ssh_key

access_key="AKIAZDSHKL5YXWF44MRK"
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

cp /home/ubuntu/ssh_key.pub /home/ubuntu/bucket/ssh_key.pub
eval `ssh-agent`
ssh-add /home/ubuntu/bucket/Hithesh_KeyPair.pem

cd /home/ubuntu/bucket
chmod +x ./script.py
python3 ./script.py
