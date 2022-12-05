import os
import array
import numpy as np
import variables
import time

WorkerNodesNumber = variables.WorkerNodesNumber
WorkerNodeType = variables.WorkerNodeType
frames = variables.frames
nodes = variables.nodes

for i in range(0, len(frames)):
      frames[i]=int(frames[i])
frames = np.array_split(frames, nodes)
IP=[]

for i in range(0,nodes+1):
  IP.append(f"172.31.32.1{i}")

nl="\n"
ansible="/etc/ansible/ansible.cfg"
hosts="/etc/ansible/hosts"
playbook="/etc/ansible/playbook.yaml"
ssh_config="/root/.ssh/config"

# Creating SSH Config file
if os.path.exists(ssh_config):
    os.remove(ssh_config)

file = open(ssh_config, 'a')
file.write("""Host *
  StrictHostKeyChecking no""")
file.close()

# Creating and Editing ansible.cfg file
if os.path.exists(ansible):
    os.remove(ansible)

file = open(ansible, 'a')
file.write("[defaults]\n")
file.write(f"forks = {nodes+1}\n")
file.write("callback_whitelist=profile_tasks\n")
file.write("remote_user=ubuntu")
file.close()

# Creating and Editing hosts file
if os.path.exists(hosts):
    os.remove(hosts)

file = open(hosts, 'a')

string = f"localhost ansible_host={IP[0]} ansible_connection=local "
for i in range(0,nodes+1):
  string1=f"IP{i}={IP[i]} "
  string = string+string1

file.write(string)
file.write("\n")
file.write("[worker_nodes]\n")
for i in range(0,nodes):
  file.write(f"worker{i+1} ansible_host={IP[i+1]} ansible_connection=ssh IP0={IP[0]} frames={frames[i][0]}..{frames[i][-1]}{nl}")

file.close()

# Creating and Editing playbook file
if os.path.exists(playbook):
    os.remove(playbook)

file = open(playbook, 'a')
file.write("""- name: playbook
  hosts: worker_nodes
  strategy: free
  remote_user: ubuntu
  become: true
  tasks:
    - name: start the rendering process by running blender in background
      command: blender -b /home/ubuntu/bucket/rendered-output/blenderfile.blend -E CYCLES -F PNG -f {{frames}} -o ./####.png
    - name: delete the script cache in the bucket
      command: rm -r /home/ubuntu/bucket/__pycache__
- name: localHostPlaybook
  hosts: localhost
  strategy: free
  remote_user: ubuntu
  become: true
  tasks:
    - name: shutdown all the running instances
      command: python3 /home/ubuntu/bucket/shutdown.py""")
file.close()

for i in range(1,nodes+1):
  os.system(f"aws ec2 run-instances --count 1 --instance-type t2.micro --key-name Hithesh_KeyPair --image-id ami-03f6a95dc53332d8f --subnet-id subnet-0ecf3e0415f17269c --security-group-ids sg-032c9ffd760342249 --instance-initiated-shutdown-behavior terminate --private-ip-address 172.31.32.1{i} --user-data file://WorkerUserData.sh")

time.sleep(120)
os.system("ansible-playbook /etc/ansible/playbook.yaml")
