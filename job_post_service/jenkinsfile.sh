#!/bin/sh -x

shared_dir=/home/sharedFolder
virtual_dir=/home/sharedFolder/tempenv
project_dir=$WORKSPACE/job_post_service

clean_up()
{
    #deactivate virtualenv
    INVENV=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')
    if [ ${INVENV} -eq 1 ]; then
        echo "deactivate tempenv"
        deactivate || { echo "deactivation failed"; return 1; }
        echo "deactivation successful"
    fi

    echo "Virtual Environment Removal"
    if [ -d ${virtual_dir} ]; then
        echo "removing virtual environment directory"
        rm -r ${virtual_dir} || { return 1; }
        echo "removal successful"
    else
        echo "${virtual_dir} does not exist"
    fi

    return 0
}

finish()
{
    echo $1
    echo "starting cleanup"
    clean_up || { echo "clean up unsuccessful"; exit 1; }
    echo "clean up completed"
    exit $2
}


echo "step 1: Create Virtual Environment"
virtualenv ${virtual_dir}  || { finish "Virtualenv failed" 1; }

echo "step 2: Activate Virtual Environment"
. ${virtual_dir}/bin/activate || { finish "Activation failed" 1; }

echo "step 3: Navigate to Project Directory"
if [ -d ${project_dir} ]; then
    cd ${project_dir};
else
    finish "Project directory does not Exist" 1
fi

INVENV=$(python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')
if [ ${INVENV} -eq 1 ]; then
    echo "step 4: Upgrade pip setup tools wheel in Virtual Environment"
    pip install --upgrade pip setuptools wheel || { finish "Upgrade failed" 1; }

    echo "step 5: Install Virtual Environment with required packages"
    pip install -r ${project_dir}/requirements-vendor.txt || { finish "Install PKG failed" 1; }

    echo "step 6: Install app with needed library"
    pip install -r ${project_dir}/requirements-vendor.txt -t ${project_dir}/lib/ || { finish "Install lib PKG failed" 1; }

    echo "step 7: generate static files"
    echo yes | python manage.py collectstatic || { finish "collect staticfiles failed" 1; }

    echo "step 8: authorize jenkins to gcloud"
    gcloud auth activate-service-account --key-file=${shared_dir}/deployKey.json || { finish "authorizing jenkins failed" 1; }

    echo "step 9: deploy"
    echo Y | gcloud app deploy || { finish "deploy to app engine failed" 1; }

    echo "step 9: VirtualEnv Cleanup"
    finish "Initiate final step cleanup" 0
fi
