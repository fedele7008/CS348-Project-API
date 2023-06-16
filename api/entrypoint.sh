#!/bin/bash

################################################################
# This script is used for docker environment
################################################################

cd src # current dir "/app/src/"

# Run flask migration upgrade
flask db upgrade
flask seed all

cd .. # current dir "/app/"

# Run the rest of the scripts
exec "${@}"
