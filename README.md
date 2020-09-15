# RGate
API Gateway for Python to link to docker containers based on a backend config.

# Installation

## Requirements
  - python 3.8
  - pip
  
## Using virtualenv
From the repository root:

    virtualenv ./env
    source ./env/bin/activate
    pip install -U -r requirements.txt
    
Activate your virtualenv, then use `python` from the env to launch the application as described below.

# Usage

## Setting up dummy backends
This repo comes pre-configured with two backends, orchestrated by `docker-compose`.

You'll need to start off with `docker-compose build`, then follow with `docker-compose up`. This sets up necessary labels
and port mapping.

## Running RGate
See `python rgate.py --help`, or:

    python rgate.py --port 8080 --config ./cfg.yaml
    
Note: RGate will fail at startup if there are no containers to serve a backend. The error should be clear. If a container
fails *after* start-up, requests to that backend will receive a 503.

## Testing it out

    curl localhost:8080/api/payments
    curl localhost:8080/api/payments/some_path
    curl localhost:8080/api/orders/

