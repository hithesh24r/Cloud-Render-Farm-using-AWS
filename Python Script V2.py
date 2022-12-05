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

IP=[]

for i in range(0,nodes+1):
  IP.append(f"172.31.32.1{i}")

print(IP)

nl="\n"

ansible="/etc/ansible/ansible.cfg"
hosts="/etc/ansible/hosts"
playbook="/etc/ansible/playbook.yaml"
ssh_config="/root/.ssh/config"

# Creating SSH Config file
if os.path.exists(ssh_config):
    os.remove(ssh_config)

file = open(ssh_config, 'a')
file.write("Host *")
file.write("  StrictHostKeyChecking no")
file.close()

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
file.write("- name: playbook\n")
file.write("  hosts: worker_nodes  \n")
file.write("  strategy: free\n")
file.write("  remote_user: ubuntu\n")
file.write("  become: true\n")
file.write("  tasks:\n")
file.write("    - name: send blenderfile.blend from master to worker nodes\n")
file.write("      copy: \n")
file.write("        src: /home/ubuntu/blenderfile.blend\n")
file.write("        dest: /home/ubuntu/\n")
file.write("        mode: '0644'\n")
file.write("    - name: Start the rendering process by running Blender in background\n")
file.write("      command: blender -b /home/ubuntu/blenderfile.blend -E CYCLES -F PNG -f {{frames}} -o /home/ubuntu/rendered_output\n")
file.write("- name: localhost_playbook\n")
file.write("  hosts: localhost\n")
file.write("  remote_user: ubuntu\n")
file.write("  become: true\n")
file.write("  tasks:\n")
file.write("    - name: Sending files to master node from worker node through Secure Copy or SCP Protocol\n")
file.write("      command: scp ubuntu@{{item}}:/home/ubuntu/*.png /home/ubuntu\n")
file.write("      loop:\n")

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
