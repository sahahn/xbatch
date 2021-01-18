#!/bin/sh
python set_config.py

# Add to bashrc
echo -e "alias xbatch='python `pwd`/xbatch.py'" >> ~/.bashrc

# Replace shell with new shell, s.t., new command is added this run
exec bash