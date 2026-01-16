# Legacy SIPin SIP Creator

## Synopsis

A service that takes version 0.1 (essence-sidecar pair or
essence-collateral-sidecar triple) SIPs and converts them to meemoo version
1.0 SIPs.

1. The input for this service is a watchfolder-message on a RabbitMQ queue
indicating newly created essence-sidecar (or essence-collateral-sidecar)
files on the FTP server.

2. Based on the watchfolder-message, the newly added version 0.1. SIP is
parsed and transformed to adhere to the version 1.0 SIP specification.

3. The output of this service is either:
    - **Success**: A new zipped version 1.0 SIP and a Pulsar event on the
    `be.meemoo.sipin.sip.create` topic which contains information
    pertaining to the newly created SIP.
    - **Failure**: A Pulsar event on the `be.meemoo.sipin.sip.create` topic
    which details what went wrong.

## Prerequisites

- Git
- Docker (optional)
- Python 3.10+
- Access to the meemoo PyPi

## Usage

Clone this repository with:

`$ git clone git@github.com:viaacode/legacy-sipin-sip-creator.git`

Change into the new directory:

`$ cd legacy-sipin-sip-creator`

Set the needed config:

Included in this repository is a config.yml file detailing the required
configuration. There is also an .env.example file containing all the needed
 env variables used in the config.yml file. All values in the config have
 to be set in order for the application to function correctly. You can use
 !ENV ${EXAMPLE} as a config value to make the application get the EXAMPLE
  environment variable.

### Run locally

1. Start by creating a virtual environment:

`$ python -m venv venv`

1. Activate the virtual environment:

`$ source venv/bin/activate`

1. Install the external modules:

```
$ pip install -r requirements.txt \
    --extra-index-url http://do-prd-mvn-01.do.viaa.be:8081/repository/pypi-all/simple \
    --trusted-host do-prd-mvn-01.do.viaa.be
```

1. Make sure to load in the ENV vars.

2. Run the tests with:

`$ python -m pytest -v --cov=./app`

1. Run the application:

`$ python -m main`

### Run using Docker

Build the container:

`$ docker build -t legacy-sipin-sip-creator .`

Run the tests in a container:

```
$ docker run \
    --env-file .env.example \
    --rm \
    --entrypoint python \
    legacy-sipin-sip-creator:latest -m pytest -v --cov=./app
```

Run the container (with specified .env file):

`$ docker run --env-file .env --rm legacy-sipin-sip-creator:latest`
