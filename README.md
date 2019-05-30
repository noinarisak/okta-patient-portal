# okta-patient-portal
Doctor, Caregiver, Patient portal for managing patient info and events protected with Okta

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites (WIP)

_Docker-Compose_ option (__preferred__)
* Docker | MacOS - [Docker for Mac Instructions](https://docs.docker.com/docker-for-mac/install/)
* Follow [setup-with-docker](./setup-with-docker.md) instructions or use [`make`](#usage).

_Non Docker-Compose_ option
* [Pipenv](https://docs.pipenv.org/)
* Follow [setup-without-docker](./setup-without-docker.md) instructions.

What things you need to install the software and how to install them

```sh
$

```

Okta tenant setup to fill in environment configuration.

1. Login to okta.
1. Use terraform to create Okta

### Usage

A step by step series of examples that tell you how to get a development env running

Outline makefile target commands

#### General

```sh
$ make help
```

#### Running / Stopping / Logging

```sh
$ make run
```

Access the application at the address [http://localhost:5002/](http://localhost:5002/)

```sh
$ make stop
```

```sh
$ make log
```

#### Testing

Test without coverage:

```sh
$ make test

```

Test with coverage:

```sh
$ make cov
```

Lint:

```sh
$ make lint
```

End with an example of getting some data out of the system or using it for a little demo


## Notes (WIP)

Add additional notes about how to deploy this on a live system

Viewing base64 ID_TOKEN and TOKEN

* Copy & Paste either ID_TOKEN or TOKEN from Cookie Session
    * Right-click > Inspect > Application > Cookie Session.
* Navigate to https://www.jsonwebtoken.io/
* Paste JWT encoded value and view the decoded JSON values.


## Authors

* **srecinto@gmail.com** - *Initial work*
* **noi.narisak@gmail.com** - *Engineer*

See also the list of [contributors](https://github.com/srecinto/okta-patient-portal/contributors) who participated in this project.


## Acknowledgments

* Generated from [cookiecutter-flask-sketeton](https://github.com/realpython/cookiecutter-flask-skeleton) and extended.
* [gitignore.io]()
