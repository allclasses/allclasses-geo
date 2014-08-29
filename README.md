Allclasses Geo Services
-----------------------

## API Use

### Geocode

```bash
$ curl -H 'Authorization: myToken' \
       -d '{"location": "109 Kingston Street, Boston MA"}' \
       http://localhost:5050/geocode/
```

### Reverse Geocode

```bash
$ curl -H 'Authorization: myToken' \
       -d '{"latitude": 42.3495585006773, "longitude": -71.0503819575293}' \
       http://localhost:5050/reverse/
```


## Development Environment

Install memcached:

```bash
# For example, on OSX
$ brew install memcached
```

Install foreman:

```bash
$ sudo gem install foreman
```

Add `local.py` to geo settings and point to a POSTGIS db.  See
`geo/settings/default.py` for an example of how to set that up.

Install pip and virtualenv, and set up dependencies:

```bash
$ virtualenv virtualenv
$ virtualenv/bin/pip/install -r requirements.txt
```

Run the service locally:

```bash
$ foreman start
```


## Deploying

Install [fabric](http://www.fabfile.org/) and define your ssh config to have
an alias for the machine you want to deploy to.

Put the settings you want on the deployment machine in `geo/settings/deploy.py`
and then

```bash
$ fab deploy:host=hostname
```

Note the neither memcached nor POSTGis are configured by the puppet
provisioning step, so you will reasonably need to have those already running
