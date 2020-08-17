# GisFIRE-API
API to manage gisfire data

## Setup (general)

### 1. Create a postgres cluster

```bash
$ sudo pg_createcluster -d /home/postgresql-12/gisfire -l /home/postgresql-12/gisfire/gisfire.log -p 5433 --start --start-conf auto 12 gisfire
```
The cluster has to be set up in the UTC timezone:

```bash
$ sudo nano /etc/postgresql/12/gisfire/postgresql.conf  
```

and set the line:

```bash
timezone = 'utc'
```

### 2. Create a gisfire database user

```bash
$ sudo -i -u postgres
$ createuser -p 5435 -P gisfireuser
$ exit
```

### 3. install

```bash
$ sudo apt-get install python3-flask-*
$ sudo pip3 install --upgrade pip
$ sudo pip3 install --upgrade Flask-HTTPAuth
$ sudo pip3 install configparser
$ exit
```
possible conflict on ubuntu 20.04 and HTTPAuth, better install pip3 newer version
on 18.04 there is no problem
