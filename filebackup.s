#!/bin/bash

rsync -av --delete --ignore-errors --exclude="Gau*" --exclude="*chk" --exclude="CHG*" --exclude="WAVECAR" -L -e ssh /home/scoombs/ scoombs@hopper.westgrid.ca:~/data/backups/mycomputer/weekly/
