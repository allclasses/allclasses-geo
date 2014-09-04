Allclasses Geo Services
-----------------------

## API Use

### Geocode

```bash
$ curl -H 'Authorization: myToken' \
       -d '{"location": "109 Kingston Street, Boston MA"}' \
       http://localhost:5050/geocode/

{
  "result": {
    "rating": 1,
    "city": "Boston",
    "region": "MA",
    "longitude": -71.0594645986262,
    "street_num": "109",
    "street_name": "Kingston",
    "street_type": "St",
    "postal_code": "02111",
    "latitude": 42.3524373067332
  }
}
```

### Reverse Geocode

```bash
$ curl -H 'Authorization: myToken' \
       -d '{"latitude": 42.3495585006773, "longitude": -71.0503819575293}' \
       http://localhost:5050/reverse/

{
    "result": {
        "rating": null,
        "city": "Boston",
        "region": "MA",
        "longitude": -71.0503819575293,
        "street_num": "49",
        "street_name": "Melcher",
        "street_type": "St",
        "postal_code": "02210",
        "latitude": 42.3495585006773
    }
}
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

Put the settings you want on the deployment machine in `geo/settings/deployment.py`
and then

```bash
$ fab deploy:host=ssh_config_alias
```

Note that neither memcached nor POSTGIS are configured by the puppet
provisioning step, so you will reasonably need to have those already running
somewhere and have your deployment settings point to them
