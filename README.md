## Currently: pkg listners/senders and deployment server setup

two versions of listener/sender
* directly using sockets 
* scanning destination directories

Currently using scan destination directory method since it was simpler to get up and running. If sockets are necessary then no problem, just more research is needed with ssh key exchange while interfacing with the incoming scp message on the port. 

Scanning destination directories allows the listener to be removed from the key exchange, however if the outgoing packages from deployment server are automated, there will still be key exchange implementation on the sender script. Time will tell whats easiest / necessary.

Currently making some assumptions about the database schema and yaml format that will be inside package.tar.gz. Everything can be adapted according to how things go and whats needed. Just needed a starting point.

![sampletable](img/table_sample.png)
![sampleyaml](img/sample_yaml.png)
