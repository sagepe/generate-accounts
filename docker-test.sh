#!/bin/bash
docker run --rm -v "$PWD":/test sagepe/accounts-test:0.2 python /test/generate_accounts.py
