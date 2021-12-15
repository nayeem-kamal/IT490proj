# Deployment Server

## Package Tool

### Instructions:

For Dev usage:

1. Download pack_tool folder

Where ever you place the folder will be where it's path is when installed. So pick a spot a keep it there.

2. Run setup.sh
```
./setup.sh
```

Running the script will:
- install req python libs
- place tool path in bashrc
- make proper directory structure for tool in (~/.config/packtool/)
- constructs the packtool config file

Now close current terminal and reopen a fresh terminal.

To check install, type:
```
pack
```

This should bring up the subcommand documentation

3. Commands

Before making a package, set project root folder:
```
pack setroot ~/folder/project_folder/
```

To make a package:
```
pack make samplepak-1.0 file1.py file2.html file3.css
```

Package name must conform to pkg naming convention 'pkgname-2.3'. The make command makes the package and sends it to the deployment server.


## Server Setup Directions

### OS
fresh ubuntu 20.04 LTS
```
sudo apt update
sudo apt upgrade
```

### Dependencies

* sudo apt install `git`
* sudo apt install `mysql-server`
* sudo apt install `openssh-server`
* sudo apt install `python3-pip`
* pip3 install `mysql-connector-python`


1. pull branch from github

1. run setup.sh for packtool
```
./setup.sh
```

Where ever you place the packtool folder will be where it's path is when installed. So pick a spot a keep it there.

1. copy packages dir structure to ~, this is where the packages will be stored
```
cp -r packages ~
```

check hosts.yaml to ensure accurate host information

1. Copy listener.service to systemd

Change user and script path inside listener as necessary

```
sudo cp listener.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable listener.service
sudo systemctl start listener.service
```
----

### MySQL Database

in MySQL:
```
create database deployment;
create user 'deploy'@'localhost'
grant select, update, delete, insert on deployment.* to deploy@localhost;
```

load .sql file into db
```
mysql -u root -p deployment < /path/deployment.sql
```




