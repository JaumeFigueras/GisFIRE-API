# GisFIRE-API


## Testing

### 1. install

```bash
$ sudo apt-get install python3-pytest python3-testing.postgresql
$ sudo pip3 install responses
$ exit
```


### run

```bash
$ pytest-3 -v -s
$ pytest-3 --cov=GisFIRE-API GisFIRE-API/test
$ pytest-3 --cov-report html:cov_html --cov=GisFIRE-API GisFIRE-API/test
```
