# GisFIRE-API
API to manage gisfire data

## Setup (general)

### 1. Create a postgres cluster

```bash
$ sudo mkdir -p /home/db/postgres/gisfire
$ sudo chown postgres:postgres /home/db/postgres/gisfire
$ sudo pg_createcluster -d /home/db/postgres/gisfire -l /home/db/postgres/gisfire/gisfire.log -p 5435 --start --start-conf auto 10 gisfire
```
The cluster has to be set up in the UTC timezone:

```bash
$ sudo nano /etc/postgresql/10/gisfire/postgresql.conf  
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
$ sudo pip3 install Flask-HTTPAuth
$ sudo pip3 install configparser
$ exit
```
poccible conflic on ubuntu 20.04 and HTTPAuth, better install pip3 newer version
on 18.04 there is no problem
