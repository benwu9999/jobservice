#!/bin/sh

echo "step 1: Create Virtual Environment"
virtualenv /home/sharedFolder/tempenv

echo "step 2: Activate Virtual Environment"
. /home/sharedFolder/tempenv/bin/activate
which python

echo "step 3: Upgrade pip setup tools wheel in Virtual Environment"
pip install --upgrade pip setuptools wheel

echo "step 4: Install Virtual Environment with required packages"
pip install -r $WORKSPACE/job_post_service/requirements-vendor.txt

echo "step 5: Install app with needed library"
pip install -r $WORKSPACE/job_post_service/requirements-vendor.txt -t ./job_post_service/lib/

echo "step 6: generate static files"
cd $WORKSPACE/job_post_service
echo yes | python manage.py collectstatic

echo "step 7: authorize jenkins to gcloud"
gcloud auth activate-service-account --key-file=/home/sharedFolder/deployKey.json

echo "step 8: deploy"
echo Y | gcloud app deploy

echo "step 9: VirtualEnv Cleanup"
deactivate
rm -r /home/sharedFolder/tempenv

