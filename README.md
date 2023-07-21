    Rendering is the process of converting a 3D project into a 2D representable format like an image or a video. This rendering process requires a lot of computational and graphical power to perform various calculations required to analyze light bounces, light paths, reflections, refractions, rigid body dynamics, fluid and smoke simulations etc. There is a growing demand for high-quality 3D models and animations for scientific simulations that visualize outcomes using 3D visuals. Better 3D models, such as those with more sophisticated geometry and photo-realistic rendering, require more time and computer capacity to produce. The rendering process presupposes that time and processing capacity are inversely proportional: the lesser computational power, the longer it takes to render, and on the other hand, the more power, the faster it takes to render. Render farms emerged to solve this issue. The render farms are deployed in some private servers, and they take the 3D file from the user, render it in their servers and send back the rendered output. And they charge the user based on number of frames rendered and how complex the rendered frames are. The only problem with this kind of render farms is that the cost is high. So, every individual can't afford a render farm to render their frames. To solve this issue, we came up with an effective way to implementing render farm over the cloud (AWS), which would be way cheaper compared to traditional render farms.
    There are a set of processes involved inside the 3D Software. The only thing that can be transferred into a different environment is the rendering part as that is the only part where any human interaction is not required. Also, that is the only process that requires the highest amount of graphical and computational power. The project would be completed over the personal computer, and it is sent to the render farm. This is the same way as the other render farms work. Here, we send the file over the cloud where the rendering is performed in an efficient way which would in turn cost us less. The rendering process will be completed over the cloud, and we can access the rendered output of the project. Deploying the render farm over the cloud has many advantages, they are:
- In the cloud computing, we can change the type of instance any time we want, so that we can use a powerful computer when required and use a low powered one when the computational power is not required.
- Rendering process is performed using the concept of cluster computing, where a set/cluster of computers divide the main task among themselves and work parallelly to complete the work faster and with more efficiency
![image](https://github.com/hithesh24r/Cloud-Render-Farm-using-AWS/assets/75219792/570a6d38-94b5-41a7-a9ac-bbbe298503ca)
    There are three kinds of nodes used in this cluster. The first one is the Master node. This is the only node by which users can interact. This node takes the project file and the required details like frames to rendered, etc, analyses and divides the task into subtasks based on the number of worker nodes, and then sends the work along with the project file to respective worker nodes. The worker nodes are the ones who are going to perform the process of rendering. Worker nodes receive their task from the master node, render the specific frames and return the output to the master node again. Here the worker node also sends the frames to the backup node. The role of backup node is to maintain a copy of all the rendered files sent from worker node to the master node, in case of any data discrepancy in the master node or the worker node after the process gets completed.

    Ansible automates remote system management and maintains the desired state of the systems. There are three key parts to an Ansible environment at its core. The first is the control node on which Ansible is installed, and all the other nodes are controlled via this node. Next one is the managed node which is a remote system that Ansible from the Control node controls. Finally, the inventory, which is a file in the control node that lists all the managed nodes(hosts). Ansible operates by establishing connections with nodes on a network and then delivering each node a little program called an Ansible module. Ansible runs these modules over SSH, and after they are done, they are deleted. The managed nodes must allow login access from your Ansible control node for this interaction to work. The most popular method of granting access is through SSH keys; however other types of authentications are also available.
    The Secure Copy Protocol or “SCP” helps to transfer computer files securely from a local to a remote host. The SCP runs on Port 22. SCP transfers the files from one node to another with authentication and security added to that. So, the data that is being transferred remains confidential, and hence the SCP can be used to successfully block packet sniffers that can extract valuable information from the data packets.
![image](https://github.com/hithesh24r/Cloud-Render-Farm-using-AWS/assets/75219792/c25740da-cba0-486f-a6aa-f11855850859)
    As we are working on cloud instances, there is a risk of data leakage or insecurity. This can be avoided by using a Virtual Private Cloud in AWS as shown in Fig. 2. As stated earlier, in VPC, the computers don’t have any relation with the other computers on the same server and a security group added to the VPC, will restrict the access of certain IP Addresses over certain ports.
