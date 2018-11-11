# Montoring resources OpensStack 

Write your own check to monitor resources in OpenStack

<img src="https://i.imgur.com/h1fQnGV.png">

## 1. Prepare

- Zabbix server:
    + Version: 3.0
    + OS: CentOS7
    + IP: 10.10.10.174
- OpenStack Queens
    + OS: CentOS7
    + IP controller: 10.10.10.175
    + Two node compute and One node cinder 

You can install via links reference: 
- <a href="https://github.com/congto/openstack-tools/tree/master/scripts/OpenStack-Queens-No-HA/CentOS7">Install OpenStack Queens</a>
- <a href="https://www.zabbix.com/documentation/3.0/manual/installation/install_from_packages/server_installation_with_mysql">Install Zabbix server</a>

**Describe**: The plugin installed in your controller node. It get metric from OpenStack and send to zabbix server via api. 

## 2. Install

### In dashboard, You create items:

- Download templates openstack and import to zabbix server

### In controller node:

- Setup python3:

    ```
    yum -y install https://centos7.iuscommunity.org/ius-release.rpm
    yum -y install python35u
    yum -y install python35u-pip
    yum install python35u-devel -y
    ```

#### Install from source:

- Clone source code:

    ```
    https://github.com/hocchudong/plugin_zabbix_openstack.git
    ```
- Update configuration in `etc/config.cfg` of source code and copy it to `/etc/openstack_monitoring/config.cfg`

- Go to openstack_monitoring and install package in file `requirements.txt`

    `pip3.5 install -r requirements.txt`

- Go to openstack_monitoring and run command:

    `python3.5 main.py start|stop|restart`

#### Install from file setup.py

- Edit `config.cfg` in `etc/config.cfg`

- Go to source code:

    `python3.5 setup.py install`

## Features

- TO DO


