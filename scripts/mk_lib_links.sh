#! /bin/bash

ENV=$(cat env_dir.txt)
LIB_BASE=$ENV/lib/python2.7/site-packages

rm -Rf gaenv/*
linkenv -i gaenv_ignore.txt $LIB_BASE gaenv
