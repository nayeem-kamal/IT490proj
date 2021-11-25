#!/bin/bash

pip3 install fire
echo 'export PATH="'$PWD':$PATH"' >> ~/.bashrc
source ~/.bashrc
chmod +x pack.py
mkdir -p ~/.config/packtool
echo "tmp_path: $PWD/tmp/" >> ~/.config/packtool/config.yaml

