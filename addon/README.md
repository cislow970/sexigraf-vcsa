# SexiGraf addon for VCSA monitoring (tested on release 0.99i)

The original SexiGraf project has been enhanced by adding vCenter monitoring via SNMPv2c or SNMPv3 protocol and REST API.
For each connected vCenter Appliance (VCSA) it's possible to monitor:

* Uptime
* Current build installed
* Available updates
* Sub-systems health
* Services health
* VCHA cluster (a three-node cluster consisting of an active, passive and witness node) health status, current active node and warning messages history (last 30 days)
* CPU usage overall and by Cores
* Load average
* Active processes
* Memory usage
* Network bandwidth utilization on public and heartbeat ethernet interface
* All file systems and external shares usage (ex.: NFS mount point)
* Latest backup status
* Content Libraries Subscribed synchronization status
* Expiration time for critical SSL certificates

# Documentation

[SexiGraf web site project](https://www.sexigraf.fr/)

# Architecture

Original architecture:

!['Original architecture'](images/sexigraf_orig_arch.jpg)

Solution added to SexiGraf for VCSA monitoring:

!['Integration for VCSA'](images/sexigraf_enhanced_arch.jpg)

The SexiGraf appliance must be able to communicate with the following ports:

* UDP 161 (SNMP Agent)
* TCP 443 (vCenter Service)
* TCP 22 (SSH)

Telegraf acquires SNMP metrics but also checks critical SSL certificates on TCP ports 443,7080 (7080 only from localhost) and verifies the mapping of logical volumes by SSH connection (TCP port 22).  

# Installation Addon

Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

# Configuration Addon

## Change default shell for root user on VCSA

Edit **/etc/password** file and change root user shell from */bin/appliancesh* to */bin/bash*.

## Configure SNMP agent on VCSA

**The SNPM v2c and v3 protocols are alternatives.**

* Configure SNMP v2c protocol

	Launch **appliancesh** shell and submit the following commands:

	1. Verify configuration agent: ``snmp.get``
	2. Enable snmp agent: ``snmp.enable``
	3. Setting community name: ``snmp.set --communities public``    
		*(public is just a sample community, you can set the community you want to use in your network, you should write it down and enter it in the configuration of the [connection to the vCenter](https://.../tree/master/sexigraf#add-connection-to-vcsa-in-sexigraf-web-admin-gui-enhanced) in SexiGraf)*
	4. Check again configuration agent: ``snmp.get``

* Configure SNMP v3 protocol

	Launch **appliancesh** shell and submit the following commands:

	1. Verify configuration agent: ``snmp.get``
	2. Enable snmp agent: ``snmp.enable``
	3. Remove communities if present (to disable the v2c protocol): ``snmp.set --communities ""``
	4. Set authentication protocol: ``snmp.set --authentication SHA1``
	5. Set privacy protocol: ``snmp.set --privacy AES128``
	6. Set password for authentication and privacy: ``snmp.hash --auth_hash secret1 --priv_hash secret2``    
		*(secret1 and secret2 are respectively your passwords for auth and priv, you should write them down and enter them in the configuration of the [connection to the vCenter](https://.../tree/master/sexigraf#add-connection-to-vcsa-in-sexigraf-web-admin-gui-enhanced) in SexiGraf)*
	7. Set user for SNMP v3: ``snmp.set --user userid/secret1/secret2/priv``    
		*(userid is the user you defined for the encrypted and authenticated connection to SNMP v3 agent, you should write it down and enter it in the configuration of the [connection to the vCenter](https://.../tree/master/sexigraf#add-connection-to-vcsa-in-sexigraf-web-admin-gui-enhanced) in SexiGraf)*
	8. Check again configuration agent: ``snmp.get``  

## Create and configure monitor user on VCSA

1. Configure monitor user for SexiGraf:

	1. Launch **appliancesh** shell and submit the following command:  
	``localaccounts.user.add --role operator --username monitor --password``    
		*(enter password equal to M0n1t0r! or whatever you want but as long as it meets the complexity criteria of the VCSA)*

	2. Exit from **appliancesh** and submit the following commands:  
	``mkdir -p /home/monitor/.ssh``  
	``touch /home/monitor/.ssh/authorized_keys``  
	``chmod 700 /home/monitor/.ssh/``  
	``chmod 600 /home/monitor/.ssh/authorized_keys``  
	``chown -R monitor:users /home/monitor/.ssh/``  

2. Edit **/etc/password** file and change monitor user shell from */bin/appliancesh* to */bin/bash*.

## Configure SexiGraf public key on VCSA

Edit file **/home/monitor/.ssh/authorized_keys** and add RSA key of telegraf user on SexiGraf (example):

``ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDHH34hzRsItP9rXYyx1kz5hlApXr/LaWL5ODnf8HK1M3B1HoZ/bVL5T8uVBc4ipNiog04l2CfWMXyxa1tIcRG5IsDrR//RPDe4gauPYvb74LIEga4D+0TGy6nUgLPEMPxTeX2ry7SpS54rWz4ccQ2m4Q0gtqKutbKYkioUplsjshKGICsyN5iKmsIm2sJ2w2INvTRRyRZwynPjOJ7XVUaiPNsvpnkP5qRup7uOVOVlW4vo/X66fsu7CA4q8yGmE3v5QP9pgeAfZ6/PhJ5I6K7CMvDZu4YrX5+FxwI5nZrKy49SdqXV0pbegnbqR3lSFngz8XvRCDBvseeZ42yl0mFNos30owSm6r9H97tTSssQao7QgZdTm6evbbkNm/TDst+GiVKsg/lADUODMAhaqbxJ/8uzHIMS8tLmLvNCpC1T2z4nHNGVOAeF46HOyQWRKxFwsvP/tgoVkuMqyEm3Y/wPhvmAwxH1Ezi2yI7GtpyZMszjI8SCuyEbZJfDH/5091U= telegraf@sexigraf``

*(RSA key correct can be viewed with the command ``cat /etc/telegraf/.ssh/id_rsa.pub`` on SexiGraf appliance)*

## Enable SSH login with public key authentication on VCSA

For enabling SSH key authentication edit **/etc/ssh/sshd_config** file and add following row (or uncomment):

``PubkeyAuthentication yes``

After saving, restart SSH service:

``systemctl restart sshd.service``

## Configure python script for checking Secure Token Service Certificate on VCSA

1. Copy script **checksts_sg.py** from repository folder *vcsa/usr/local/bin/* in the path */usr/local/bin* on VCSA
2. Assign to script execution permission and ownership to **monitor** user

## Add connection to VCSA in SexiGraf Web Admin GUI (enhanced)

You can add a connection for each vCenter 8.x in your infrastructure:  

![SexiGraf Admin](images/sexigraf_addvc_1.png)
![Add vCenter connection](images/sexigraf_addvc_2.png)

## New VCSA dashboards on SexiGraf

![VCSA dashboards](images/sexigraf_vcsa_dashboards.png)  

* VCSA Health and Performance:  

![VCSA Health and Performance 1](images/sexigraf_vcsa_health_perf_1.png)
![VCSA Health and Performance 2](images/sexigraf_vcsa_health_perf_2.png)  

* VCSA Network and Storage:  

![VCSA Network and Storage 1](images/sexigraf_vcsa_network_storage_1.png)
![VCSA Network and Storage 2](images/sexigraf_vcsa_network_storage_2.png)
![VCSA Network and Storage 3](images/sexigraf_vcsa_network_storage_3.png)
![VCSA Network and Storage 4](images/sexigraf_vcsa_network_storage_4.png)  

* VCHA cluster:  

![VCSA HA cluster 1](images/sexigraf_vcsa_ha_1.png)  
![VCSA HA cluster 2](images/sexigraf_vcsa_ha_2.png)  

* VCSA Backup:  

![VCSA Backup](images/sexigraf_vcsa_backup.png)  

* VCSA Content Library:  

![VCSA Content Library](images/sexigraf_vcsa_clib.png)  

* VCSA SSL certificates:  

![VCSA SSL certificates](images/sexigraf_vcsa_sslcert.png)  

