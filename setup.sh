#!/bin/sh
python config_setup.py

# Add to bashrc
echo -e "alias xbatch='python `pwd`/xbatch.py'" >> ~/.bashrc

echo 'Finishing up!'

# Replace shell with new shell, s.t., new command is added this run
exec bash

