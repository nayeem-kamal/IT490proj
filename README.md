
# IT490proj

The repository contains all of the necessary code files to run this Cryptocurrency Web Trading application. This was created as a project for IT490-101, Systems Integration at NJIT under Donald Kehoe. Users will be able to login into the app to trade Cryptocurrency such as Etherium and Bitcoin. They will be able to review their trade history, have portfolio tracking, recieve push notifications when they execute a trade, and see up to date charts of each cryptocurrency.  You can see technologies used in the project below.

Front End: Python, Bootstrap, HTML, CSS, Javascript <br >
Back End: Python, SQL  <br >
DMZ: Python  <br >
Data Sources: CoinMarketCap API, CryptoCompare API <br >

## Getting started:  <br >
These instructions will help you get started setting up on the local machine for whatever purpose is needed. The binding for the queues are created automatically when anything using RabbitMQ is run  <br >
----
### Setting Up <br >
### Users and Exchanges <br >
### DMZ User <br >
  Username: dmz <br >
  Password: dmz <br >
### DMZ Exchange <br >
  Exchange Type: Direct Queue <br >
### MySQL User <br >
  Username: mysql <br >
  Password: mysql <br >
### MySQL Exchanges <br >
  Exchange Type: Direct Queue <br >
### Network Logger User <br >
  Username: networklogger <br >
  Password: networklogger <br >
### Network Logger Exchanges <br >
  Exchange Type: Direct Queue <br >
### RabbitMQ
As specified you will need to get the RabbitMQ management server plugin and start the RabbitMQ instance in the browser at the specified IP address <br >
The exchanges that need to be made are specified above (NetworkLogger exchange, DMZ exchange, and MySQL exchange). The queues are automatically created and binded and they need to be direct exchanges. <br >
### Database <br >
The database topology is in the dbServer directory in the schema.sql file <br >
DB credentials are up to you but input in the database.config file in the dbAPI directory <br >
The functions for information to get stored in the SQL database are in the dbAPI directory and store in the sqlpython.py file <br >
### DMZ <br >
To run everything that you need for the DMZ go into the CoinAPI directory and python3 the CoinAPI to load the listener and logger <br >
### Front End <br > 
To run the server for the front end python3 manage.py runserver_plus --cert-file cert.pem --key-file key.pem in the /It490proj/website/kommando directory <br >
Also python3 the API.py and DB.py files in the rpcClient directory while the server is running <br >
## Running the Tests:
 -Open  branch testLogin/validation  /It490proj/website/kommando in the browser begin the testing the webpages
 ### The webpages are as follows
 
 -Login: loging with the username and password 
 
 -Register: ener personal and specifique information before gaining access to home  page
 
 -Home: display contents information after login.
 
 -Account: top bar page to access account(cash, bitcoin, ethereum)
 
 -Market trade: a top bar page to make your trade
 
 -Learn: a Learning page accessible to learn more about bitcoin, and ethereum by getting redirected to coinbase
 
 -Chart: side bard page to see the current price flow rate currency
 
 
 # Deployment Server Setup
## Deployment files are found on the deployment_server branch
## Package Tool for Dev Boxes

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


## Server Replication Setup Directions

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
````
## CoinMarketCap and CryptoCompare
The two APIs being used for free are [CoinMarketCap](https://coinmarketcap.com/) and [CryptoCompare](https://www.cryptocompare.com/) < br>

## Authors
Nayeem Kamal - Front, Back, DMZ, SQL - NHK6 <br > 
Jared Myers - Deployment, Back End - JM 297 <br >
Parnell Provilon - Front End - PDP72 <br >
James Lupo - Back End, SQL - JAL97 <br >
Ibrahima Diallo - Front End - ID55 <br >
