#!/bin/bash

FILE="$HOME/.config/packtool/config.yaml"

if [[ -f $FILE ]];then
		echo "Config detected."
		echo "Edit config directly if necessary:"
		echo "$FILE"
		exit 0
else
		pip3 install fire
		pip3 install paramiko
		pip3 install scp
		echo 'export PATH="'$PWD':$PATH"' >> ~/.bashrc
		echo "pack added to PATH in bashrc."
		source ~/.bashrc
		chmod +x pack
		mkdir -p ~/.config/packtool/tmp
		mkdir ~/.config/packtool/new_packages
		mkdir ~/.config/packtool/backup
		mkdir ~/.config/packtool/outstanding_packages
		touch $HOME/.config/packtool/logs.log
		echo "tmp_path: $HOME/.config/packtool/tmp/" >> ~/.config/packtool/config.yaml
		echo "log_path: $HOME/.config/packtool/logs.log" >> ~/.config/packtool/config.yaml
		echo "new_pkg_path: $HOME/.config/packtool/new_packages/" >> ~/.config/packtool/config.yaml
		echo "backup_path: $HOME/.config/packtool/backup/" >> ~/.config/packtool/config.yaml
		echo "outstanding_path: $HOME/.config/packtool/outstanding_packages/" >> ~/.config/packtool/config.yaml
		echo "last_pkgid: none" >> ~/.config/packtool/config.yaml
		echo "current_pkgid: none" >> ~/.config/packtool/config.yaml
		
		echo "config folder created: ~/.config/packtool/"
fi

