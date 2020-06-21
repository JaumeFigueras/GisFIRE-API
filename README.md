# GisFIRE-API
API to manage gisfire data

## Setup (general)

### 1. Create a postgres cluster

```bash
$ sudo mkdir -p /home/db/postgres/gisfire
$ sudo chown postgres:postgres /home/db/postgres/gisfire
$ sudo pg_createcluster -d /home/db/postgres/gisfire -l /home/db/postgres/gisfire/gisfire.log -p 5435 --start --start-conf auto 10 gisfire
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
