Phantom Database Manager

Phantom DBM is an open source database manager created to make it easier to manage database scripts and the process of how data is uploaded to a database. It's a program that allows the user to manage and keep track what is uploaded into their database as well as keep record of who is storing this data*. It also makes it possible to automate where the data come from without having to specify this information whenever you wish to upload data such as: data from other collection or database, information from the internet (web scraping)*, or user entered formulas.

Currently Phantom only supports MongoDB but plans to support more NoSQL databases ( and maybe sql) in the future.

Development of the program has finished and is currently being beta tested.

* to be implemented

To start program run the build.sh file:  
  
$ chmod 770 build.sh  
$ ./build.sh  
$ python3 phtm_main.py