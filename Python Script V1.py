import os
import numpy as np
import array

decision = input("How would you like to enter the frames to be rendered? \n 1. Enter frame numbers individually\n 2. Enter start and end frames\n Select either option '1' or '2': ")

if(decision=='1'):
    frames=input("Enter the frame numbers seperated by ', ': ").split(", ")
    nodes=int(input("Enter the number of worker nodes: "))

    for i in range(0, len(frames)):
      frames[i]=int(frames[i])

elif(decision=='2'):
    start = int(input("Enter the starting frame: "))
    end = int(input("Enter the ending frame: "))
    nodes=int(input("Enter the number of worker nodes: "))

    frames = np.arange(start, end+1, 1)
    frames = frames.tolist()

frames = np.array_split(frames, nodes)
print(frames)

# Defining variables
IP=[]
IP.append(input(f"Enter the IP Address for Master Node: "))
for i in range(1,nodes+1):
  IP.append(input(f"Enter IP Address for worker node {i}: "))

nl="\n"

ansible="/etc/ansible/ansible.cfg"
hosts="/etc/ansible/hosts"
playbook="/etc/ansible/playbook.yaml"

# Creating and Editing ansible.cfg file

if os.path.exists(ansible):
    os.remove(ansible)

file = open(ansible, 'a')
file.write("[defaults]\n")
file.write(f"forks={nodes+1}\n")
file.write("callback_whitelist=profile_tasks\n")
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

playbook_commands = ["- name: playbook\n",
"  hosts: worker_nodes  \n",
"  strategy: free\n",
"  remote_user: ubuntu\n",
"  become: true\n",
"  tasks:\n",
"    - name: send blenderfile.blend from master to worker nodes\n",
"      copy: \n",
"        src: /home/ubuntu/blenderfile.blend\n",
"        dest: /home/ubuntu/\n",
"        mode: '0644'\n",
"    - name: Start the rendering process by running Blender in background\n",
"      command: blender -b /home/ubuntu/blenderfile.blend -E CYCLES -F PNG -f {{frames}} -o ./####.png\n",
"- name: localhost_playbook\n",
"  hosts: localhost\n",
"  remote_user: ubuntu\n",
"  become: true\n",
"  tasks:\n",
"    - name: Sending files to master node from worker node through Secure Copy or SCP Protocol\n",
"      command: scp ubuntu@{{item}}:/home/ubuntu/*.png /home/ubuntu\n",
"      loop:\n"]

for i in range(len(playbook_commands)):
    file.write(playbook_commands[i])
    
for i in range(1,nodes+1):
  i = str(i)
  file.write('        - "{{IP' + i + '}}"\n')
file.close()

ansible_syntax_check="ansible-playbook /etc/ansible/playbook.yaml --syntax-check"
ansible_playbook_run="ansible-playbook /etc/ansible/playbook.yaml"
os.system(ansible_syntax_check)

decision = input("Are there any changes in the syntax check?  ")

if(decision=='yes'):
  print("Please check the python script and enter valid values into the input!!")
elif(decision=='no'):
  os.system(ansible_playbook_run)
else:
  print("\nPlease enter either 'yes' or 'no'!!")
