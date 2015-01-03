#! /bin/bash

ENV=$(cat env_dir.txt)

echo "Checking if virtualenv exists..."
echo ""

if [ ! -d "$ENV" ]; then
    echo "Creating virtualenv in $ENV"
    virtualenv $ENV
else
    echo "virtualenv already exists in $ENV"
fi

echo ""
echo "Installing requirements..."
echo ""

$ENV/bin/pip install -U -r requirements.txt
