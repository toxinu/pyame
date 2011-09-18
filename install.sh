#!/bin/bash
script_version="0.1"

#=============================================================================
PYHAME_VER="0.8.1.1"
PYHAME_URL="http://redmine.socketubs.net/attachments/download/12/Pyhame-$PYHAME_VER.tar.gz"

JINJA2_VER="2.6"
JINJA2_URL="http://pypi.python.org/packages/source/J/Jinja2/Jinja2-$JINJA2_VER.tar.gz"
#=============================================================================

# Globals variables
#-----------------------------------------------------------------------------

DATE=`date +"%Y%m%d%H%M%S"`

TMP_FOLDER="/tmp/pyhame-install.$DATE"
LOG_FILE="/tmp/pyhame-install-$DATE.log"

# Functions
#-----------------------------------------------------------------------------

displaymessage() {
  echo "$*"
}

displaytitle() {
  displaymessage "------------------------------------------------------------------------------"
  displaymessage "$*"  
  displaymessage "------------------------------------------------------------------------------"

}

displayerror() {
  displaymessage "$*" >&2
}

# First parameter: ERROR CODE
# Second parameter: MESSAGE
displayerrorandexit() {
  local exitcode=$1
  shift
  displayerror "$*"
  exit $exitcode
}

# First parameter: MESSAGE
# Others parameters: COMMAND (! not |)
displayandexec() {
  local message=$1
  echo -n "[In progress] $message"
  shift
  $* >> $LOG_FILE 2>&1 
  local ret=$?
  if [ $ret -ne 0 ]; then
    echo -e "\r\e[0;31m      [ERROR]\e[0m $message"
    # echo -e "\r      [ERROR] $message"
  else
    echo -e "\r\e[0;32m         [OK]\e[0m $message"
    # echo -e "\r         [OK] $message"
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
fi
}

check_python() {
PYTHON="/usr/bin/python3.2"
if [ ! -f "$PYTHON" ]; then
	PYTHON="/usr/bin/python3"
    if [ ! -f "$PYTHON"]; then
    	PYTHON="/usr/bin/python"
		PYTHON_OK=`$PYTHON -c 'import sys; print(sys.version_info >= (3, 0))'`
    	if [ "$PYTHON_OK" == False ]; then
			echo -e "You have to download Python 3.2 (http://www.python.org/getit/releases/3.2/)"
        	exit
    	fi
    fi
fi
}

# Function: installation
installation() {
  mkdir $TMP_FOLDER
  
  cd $TMP_FOLDER
  if [[ "$platform" == 'darwin' ]]; then
    displayandexec "Download Jinja2 v$JINJA2_VER" curl -O $JINJA2_URL
  else
    displayandexec "Download Jinja2 v$JINJA2_VER" wget $JINJA2_URL
  fi
  displayandexec "Untar Jinja2 v$JINJA2_VER" tar xvf Jinja2-$JINJA2_VER.tar.gz
  cd Jinja2-$JINJA2_VER
  displayandexec "Install Jinja2 v$JINJA2_VER" $PYTHON setup.py install

  cd $TMP_FOLDER
  if [[ "$platform" == 'darwin' ]]; then
    displayandexec "Download Pyhame v$PYHAME_VER" curl -O $PYHAME_URL
  else
    displayandexec "Download Pyhame v$PYHAME_VER" wget $PYHAME_URL
  fi
  displayandexec "Untar Pyhame v$PYHAME_VER" tar xvf Pyhame-$PYHAME_VER.tar.gz
  cd Pyhame-$PYHAME_VER
  if [ ! -d "/usr/lib/pyhame" ]; then
	mkdir /usr/lib/pyhame
  fi
  displayandexec "Install Pyhame v$PYHAME_VER" cp -R resources /usr/lib/pyhame/ && cp pyhame.py /usr/lib/pyhame
  echo -e '#!/bin/sh \nexec /usr/lib/pyhame/pyhame.py $1' > /usr/bin/pyhame
  displayandexec "Set Pyhame v$PYHAME_VER executable" chmod +x /usr/bin/pyhame
  
  rm -rf $TMP_FOLDER
}

# Fonction: Affiche le résumé de l'installation
end() {
  echo ""
  echo "=============================================================================="
  echo "Installation is finished"
  echo "=============================================================================="
  echo "Log for the installation script   : $LOG_FILE"
  echo "Pyhame executable                 : /usr/bin/pyhame"
  echo "Pyhame libraries                  : /usr/lib/pyhame"
  echo "Help                              : pyhame --help"
  echo "=============================================================================="
  echo ""
}

# Main program
#-----------------------------------------------------------------------------

# Check if root user is used
if [ "$(id -u)" != "0" ]; then
	echo "This script should be run as root."
	echo "Syntaxe: sudo $0"
	exit 1
fi

# Check python version
check_python
check_os
displaytitle "-- Installation"
installation
end
