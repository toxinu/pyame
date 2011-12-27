#!/bin/bash
script_version="0.3"

#=============================================================================
PYHAME_VER="0.8.3"
PYHAME_URL="http://dl.socketubs.net/pyhame/pyhame-$PYHAME_VER.tar.gz"

JINJA2_VER="2.6"
JINJA2_URL="http://pypi.python.org/packages/source/J/Jinja2/Jinja2-$JINJA2_VER.tar.gz"

SETUPTOOLS_URL="http://python-distribute.org/distribute_setup.py"
#=============================================================================

# Globals variables
#-----------------------------------------------------------------------------

DATE=`date +"%Y%m%d%H%M%S"`

TMP_FOLDER="/tmp/pyhame-install.$DATE"
LOG_FILE="/tmp/pyhame-install-$DATE.log"

function check_code {
	if [ $1 -ne 0 ]; then
		echo
		echo "Output: $2"
		echo
		exit $1
	fi
}

displaymessage () {
  echo $*
}

displayerror () {
  displaymessage "$*" >&2
}

displayerrorandexit () {
  local exitcode=$1
  shift
  displaymessage $*
  exit $exitcode
}

displayandexec () {
  local message=$1
  echo -n "[In progress] $message"
  shift
  $* >> $LOG_FILE 2>&1
  local ret=$?
  if [ $ret -ne 0 ]; then
    echo -e "\r      [ERROR] $message"
  else
    echo -e "\r         [OK] $message"
  fi
  return $ret
}

check_os() {
  platform='unknown'
  unamestr=`uname`
  if [[ "$unamestr" == 'Linux' ]]; then
    platform='linux'
  elif [[ "$unamestr" == 'FreeBSD' ]]; then
    platform='freebsd'
  elif [[ "$unamestr" == 'Darwin' ]]; then
    platform='darwin'
  else
		return 1
	fi
}

check_python () {
  PYTHON="python3.2"
	if ! which $PYTHON &> /dev/null; then
    PYTHON="python3"
		if ! which $PYTHON &> /dev/null; then
      PYTHON="python"
	  	PYTHON_OK=`$PYTHON -c 'import sys; print(sys.version_info >= (3, 0))'`
      if [ "$PYTHON_OK" == False ]; then
				return 1
			fi
		fi
	fi
}

check_module () {
	if ! $($PYTHON -c "import $1" &> /dev/null); then
		result=False
	else
		result=True
		echo -e "\r         [OK] $1 is already installed"
	fi
}

function pre_install () {
	displayandexec "Check Python 3.2 Interpreter" check_python
	check_code $? "Im so sorry.. i can't find your Python3.x interpreter.\nYou can download and install it at : http://www.python.org/getit/releases/3.2/"
	displayandexec "Check operating system" check_os
	check_code $? "Again me ? No... your slave can't find your operating system..."
}

function installation () { 
  echo " :: Installation"
	echo "    + Pre-requires"
	pre_install
	echo "    + Install"
  displayandexec "Create temp folders" mkdir $TMP_FOLDER
  check_code $? "I can't create your temp folder at: $TMP_FOLDER"
	cd $TMP_FOLDER

  check_module setuptools
  if [[ "$result" == "False" ]]; then
    if [[ "$platform" == 'darwin' ]]; then
      displayandexec "Download setuptools for Python 3.x" curl -o distribute_setup.py $SETUPTOOLS_URL
			check_code $? "I have failed.. to download a file on the Internet.\nCheck log at: $LOG_FILE"
    else
      displayandexec "Download setuptools for Python 3.x" wget $SETUPTOOLS_URL
			check_code $? "I have failed.. to download a file on the Internet.\nCheck log at: $LOG_FILE"
    fi
    displayandexec "Install setuptools for Python 3.x" $PYTHON distribute_setup.py
		check_code $? "Error during distribute, look at: $TMP_FOLDER"
  fi

  check_module jinja2
  if [[ "$result" == "False" ]]; then
    if [[ "$platform" == 'darwin' ]]; then
      displayandexec "Download Jinja2 v$JINJA2_VER" curl -o Jinja2-$JINJA2_VER.tar.gz $JINJA2_URL
			check_code $? "I have failed.. to download a file on the Internet with curl.\nCheck log at: $LOG_FILE"
    else
      displayandexec "Download Jinja2 v$JINJA2_VER" wget $JINJA2_URL
			check_code $? "I have just tried to download a file on the Internet with wget.\nCheck log at: $LOG_FILE"
    fi
    displayandexec "Untar Jinja2 v$JINJA2_VER" tar xvf Jinja2-$JINJA2_VER.tar.gz
		check_code $? "tar creates and manipulates streaming archive files. And I have failed with it...\nCheck log at: $LOG_FILE"
    cd Jinja2-$JINJA2_VER
    displayandexec "Install Jinja2 v$JINJA2_VER" $PYTHON setup.py install
		check_code $? "It's a serious error. RUN RUN... or just look at log file ($LOG_FILE).\nI have failed with \"$PYTHON setup.py install\"."
  fi

  cd $TMP_FOLDER
  if [[ "$platform" == 'darwin' ]]; then
    displayandexec "Download Pyhame v$PYHAME_VER" curl -o pyhame-$PYHAME_VER.tar.gz $PYHAME_URL
		check_code $? "I have failed.. to download a file on the Internet with curl.\nCheck log at: $LOG_FILE"
  else
    displayandexec "Download Pyhame v$PYHAME_VER" wget $PYHAME_URL
		check_code $? "I have failed.. to download a file on the Internet with wget.\nCheck log at: $LOG_FILE"
  fi
  displayandexec "Untar Pyhame v$PYHAME_VER" tar xvf pyhame-$PYHAME_VER.tar.gz
	check_code $? "tar creates and manipulates streaming archive files. And I have failed with it...\nCheck log at $LOG_FILE"
  cd pyhame/src
  if [ ! -d "/usr/lib/pyhame" ]; then
		mkdir /usr/lib/pyhame
		check_code $? "I just want to create a folder.. so rude with me.\n Check log at: $LOG_FILE"
  fi
  displayandexec "Install Pyhame v$PYHAME_VER" cp -R pyhame markdown /usr/lib/pyhame/
	check_code $? "I have tried to copy Pyhame datas to /usr/lib/pyhame.. and it's a failure.\n Look at log: $LOG_FILE"
  echo -n -e "#! $(which $PYTHON)
import sys 					 	
sys.path.append(\"/usr/lib/pyhame\")
from pyhame.pyhame import main	
if __name__==\"__main__\":			
	main()" > /usr/bin/pyhame

  displayandexec "Set Pyhame v$PYHAME_VER executable" chmod +x /usr/bin/pyhame
	check_code $? "Oh damn... Again ? Tried to make pyhame executable but... no.\nCheck log at: $LOG_FILE"
  rm -rf $TMP_FOLDER
  end_install
}

end_install() {
  echo " :: Informations"
  echo "    | Installation log : $LOG_FILE"
  echo "    | Pyhame executable: /usr/bin/pyhame"
  echo "    | Pyhame libraries : /usr/lib/pyhame"
  echo "    | Help             : pyhame --help"
  exit 1
}

remove () {
  echo " :: Clean"
  if [ -d "/usr/lib/pyhame" ]; then
    displayandexec "Remove Pyhame libs" rm -fr /usr/lib/pyhame
		check_code $? "Im an evil guy and i don't want you delete pyhame..\nSeriously i have failed to remove \"/usr/lib/pyhame\"."
	else
		echo -e "\r         [OK] Libs are already be removed"	
  fi
  if [ -f "/usr/bin/pyhame" ]; then
    displayandexec "Remove Pyhame binarie" rm -fr /usr/bin/pyhame
		check_code $? "And now... it's a failure. Just want to remove \"/usr/bin/pyhame binarie\"\nCheck log at: $LOG_FILE"
	else
		echo -e "\r         [OK] Binaries are already be removed"	
  fi
  end_remove
}

end_remove () {
	echo " :: Informations"
  echo "    | Remove log: $LOG_FILE"
  echo "    | Pyhame    : /usr/bin/pyhame, /usr/lib/pyhame"
  exit 1
}

# Main program
#-----------------------------------------------------------------------------

# Check if root user is used
if [ "$(id -u)" != "0" ]; then
	echo "This script should be run as root."
	echo "Syntaxe: sudo $0"
	exit 1
fi

showMenu () {
  echo " :: Pyhame Setup Wizard"
  echo "    + 1) Installation"
  echo "    + 2) Remove"
  echo "    + 3) Update"
  echo "    + 4) Quit"
	echo "      | Your slave ask you what you want it do:"
  read -p "      | Choice: " choice
}
  while [ 1 ]
  do
    showMenu
    case "$choice" in
      "1") installation;;
      "2") remove;;
      "3") echo "Update feature [WIP]"; exit;;
      "4") exit;;
    esac
  done
