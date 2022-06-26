#!/bin/sh
./manage.py buildstaticsite && aws s3 sync build/localhost s3://gasman.zxdemo.org/ --acl public-read --profile gasman
