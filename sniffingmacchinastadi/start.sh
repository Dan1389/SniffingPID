#!/bin/bash

cp /opt/cps/configs/config.ini /opt/cps/consensus/config.ini

cd /opt/cps/consensus

source env/bin/activate
python progetto.py 
