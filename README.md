PLSDoIt: A Feature Request App
===========================================

PLSDoIt is a feature request app. It allows creating, editing, removing and searching feature requests.
It's a Python web app that uses:

* Flask
* Flask-WTForms
* Flask-SQLAlchemy
* Bootstrap-flask
* WTForms-sqlalchemy


Here's what it looks like:

![PLSDoIt image ](https://raw.githubusercontent.com/fcorrea/plsdoit/master/Screenshot%20from%202019-05-05%2019-20-41.png)


## Table of content

- [Installation](#installation)
    - [Checkout](#repository-cloning)
    - [Running tests](#running-tests)
    - [Running PLSDoIt](#running-plsdoit)
    - [Sample Data](#sample-data)

## Installation

This document is for the latest PLSDoIt.

Make sure to have [Docker](https://www.docker.com/get-started) and [docker-compose](https://docs.docker.com/compose/install/) installed on your system.

### Checkout

Once you have verified that both docker and docker-compose are installed and working, proceed to checkout this repository with the following command:

```shell
$ git clone https://github.com/fcorrea/plsdoit
```

### Running Tests


Before running the app, it's nice to check if everything is correctly setup. Run the app tests with the following:

```shell
$ make test
```

Wait a little and verify that all tests pass. Here's the result of a successful test run:

```
app_1  | ============================= test session starts ==============================
app_1  | platform linux -- Python 3.6.7, pytest-4.4.1, py-1.8.0, pluggy-0.9.0
app_1  | rootdir: /app/app, inifile: pytest.ini
app_1  | plugins: cov-2.6.1
app_1  | collected 12 items
app_1  |
app_1  | app/tests/test_app.py ............                                       [100%]
app_1  |
app_1  | ========================== 12 passed in 9.03 seconds ===========================
```

### Running PLSDoIt

Having the confirmation the tests are passing, starting the PLSDoIt is as easy as:

```shell
$ make
```

If you want to monitor the startup sequence, run:

```shell
$ docker-compose logs -f
```

Once PLSDoIt is up, you can reach it at [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Sample Data

In order to better explore PLSDoIt capabilities, some sample data can be loaded into the database. Run the following:

```shell
$ make sample-data
```
