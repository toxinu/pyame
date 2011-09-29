#!/bin/bash
script_version="0.2"

#=============================================================================
PYHAME_VER="0.8.1.1"
PYHAME_URL="http://redmine.socketubs.net/attachments/download/15/Pyhame-$PYHAME_VER.tar.gz"

JINJA2_VER="2.6"
JINJA2_URL="http://pypi.python.org/packages/source/J/Jinja2/Jinja2-$JINJA2_VER.tar.gz"

SETUPTOOLS_URL="http://python-distribute.org/distribute_setup.py"
#=============================================================================

source /home/glehee/Repositories/pyhame/simple_curses.sh

# Globals variables
#-----------------------------------------------------------------------------

DATE=`date +"%Y%m%d%H%M%S"`

TMP_FOLDER="/tmp/pyhame-install.$DATE"
LOG_FILE="/tmp/pyhame-install-$DATE.log"

# Functions
#-----------------------------------------------------------------------------
#displaymessage() {
#  echo $*
#}

displaytitle() {
  echo "|                                                                 |"
  echo "#-----------------------------------------------------------------#"
  echo "|$*"
  echo "#-----------------------------------------------------------------#"
}

displayerror() {
  displaymessage "$*" >&2
}

# First parameter: ERROR CODE
# Second parameter: MESSAGE
displayerrorandexit() {
  local exitcode=$1
  shift
  echo "$*"
  exit $exitcode
}

# First parameter: MESSAGE
# Others parameters: COMMAND (! not |)
displayandexec() {
  local message=$1
  echo -n "| [In progress] $message                                             |"
  shift
  $* >> $LOG_FILE 2>&1 
  local ret=$?
  if [ $ret -ne 0 ]; then
    echo -e " \r\e [0;31m    [ERROR]\e[0m $message"
  else
    echo -e " \r\e [0;32m       [OK]\e[0m $message"
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
    if [ ! -f "$PYTHON" ]; then
      PYTHON="/usr/bin/python"
	  PYTHON_OK=`$PYTHON -c 'import sys; print(sys.version_info >= (3, 0))'`
      if [ "$PYTHON_OK" == False ]; then
	    echo -e "You have to download Python 3.2 (http://www.python.org/getit/releases/3.2/)"
        exit
      fi
    fi
  fi
}

check_module () {
if ! $($PYTHON -c "import $1" &> /dev/null); then
	result=False
else
	result=True
	echo -e "\r\e[0;32m         [OK]\e[0m $1 is already installed"
fi
}

# Function: installation
installation() {
  displaytitle "-- Installation                                                  |"

  mkdir $TMP_FOLDER
  cd $TMP_FOLDER

  check_module setuptools
  if [[ "$result" == "False" ]]; then
    if [[ "$platform" == 'darwin' ]]; then
      displayandexec "Download setuptools for Python 3.x" curl -0 $SETUPTOOLS_URL
    else
      displayandexec "Download setuptools for Python 3.x" wget $SETUPTOOLS_URL
    fi
    displayandexec "Install setuptools for Python 3.x" $PYTHON distribute_setup.py
  fi

  check_module jinja2
  if [[ "$result" == "False" ]]; then
    if [[ "$platform" == 'darwin' ]]; then
      displayandexec "Download Jinja2 v$JINJA2_VER" curl -O $JINJA2_URL
    else
      displayandexec "Download Jinja2 v$JINJA2_VER" wget $JINJA2_URL
    fi
    displayandexec "Untar Jinja2 v$JINJA2_VER" tar xvf Jinja2-$JINJA2_VER.tar.gz
    cd Jinja2-$JINJA2_VER
    displayandexec "Install Jinja2 v$JINJA2_VER" $PYTHON setup.py install
  fi

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
  
  end_install
}

end_install() {
  echo "#=================================================================#"
  echo "| Installation is finished                                        |"
  echo "#=================================================================#"
  echo "| Log for the installation script   : $LOG_FILE                   |"
  echo "| Pyhame executable                 : /usr/bin/pyhame             |"
  echo "| Pyhame libraries                  : /usr/lib/pyhame             |"
  echo "| Help                              : pyhame --help               |"
  echo "#=================================================================#"
  echo ""
  exit 1
}

remove() {
  displaytitle "-- Clean"

  if [ -d "/usr/lib/pyhame" ]; then
    displayandexec "Remove Pyhame libraries directorie" rm -fr /usr/lib/pyhame
  fi
  if [ -f "/usr/bin/pyhame" ]; then
    displayandexec "Remove Pyhame" rm -fr /usr/bin/pyhame
  fi
  if [ -n "$(ls /usr/lib/python3.2/site-packages/ | grep '^[jJ]inja*')" ]; then
    displayandexec "Remove Jinja2" rm -fr /usr/lib/python3.2/site-packages/{jinja2*,Jinja*}
  fi

  end_remove
}

end_remove() {
  echo "#=================================================================#"
  echo "| Clean is finished                                               |"
  echo "#=================================================================#"
  echo "| Log for the remove script : $LOG_FILE                           |"
  echo "| Removed pyhame folders    : /usr/bin/pyhame, /usr/lib/pyhame    |"
  echo "| Removed jinja2 folders : Done                                   |"
  echo "#=================================================================#"
  echo ""
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

# Check python version
check_python
check_os

  choice=$(dialog --stdout --title "Pyhame Setup Wizard" --menu "Choice :" "10" "40" "3" "1" "Installation" "2" "Remove" "3" "Update")
  case "$choice" in
    "1") installation;;
    "2") remove;;
    "3") echo "Update feature [WIP]"; exit;;
  esac