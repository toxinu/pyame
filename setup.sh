#!/bin/bash
script_version="0.2"

#=============================================================================
PYHAME_VER="0.8.1.2"
PYHAME_URL="http://dl.socketubs.net/pyhame/pyhame-$PYHAME_VER.tar.gz"
#=============================================================================

# Globals variables
#-----------------------------------------------------------------------------
DATE=`date +"%Y%m%d%H%M%S"`
TMP_FOLDER="/tmp/pyhame-install.$DATE"
LOG_FILE="/tmp/pyhame-install-$DATE.log"

# Functions
#-----------------------------------------------------------------------------
displaymessage() {
  echo $*
}

displaytitle() {
  echo "#-----------------------------------------------------------------#"
  echo "| $*"
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
  displaymessage $*
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
    # echo -e "\r   [ERROR] $message"
  else
    echo -e "\r\e[0;32m         [OK]\e[0m $message"
    # echo -e "\r      [OK] $message"
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

# Function: installation
installation() { 
  clear
  displaytitle "-- Installation"

  mkdir $TMP_FOLDER
  cd $TMP_FOLDER
  if [[ "$platform" == 'darwin' ]]; then
    displayandexec "Download Pyhame v$PYHAME_VER" curl -O $PYHAME_URL
  else
    displayandexec "Download Pyhame v$PYHAME_VER" wget $PYHAME_URL
  fi
  displayandexec "Untar Pyhame v$PYHAME_VER" tar xvf pyhame-$PYHAME_VER.tar.gz
  cd pyhame-$PYHAME_VER
  if [ ! -d "/usr/lib/pyhame" ]; then
	mkdir /usr/lib/pyhame
  fi
  displayandexec "Install Pyhame v$PYHAME_VER" cp -R * /usr/lib/pyhame/
  echo -e '#!/bin/sh \n$PYTHON /usr/lib/pyhame/pyhame.py $1' > /usr/bin/pyhame
  echo -e '#!/bin/sh \n$exec /usr/lib/pyhame/setup.sh --update' > /usr/bin/pyhame-update
  displayandexec "Set Pyhame v$PYHAME_VER executable" chmod +x /usr/bin/pyhame*
  
  rm -rf $TMP_FOLDER
  
  end_install
}

end_install() {
  echo "#=================================================================#"
  echo "| Installation is finished                                        |"
  echo "#=================================================================#"
  echo "| Installation log      : $LOG_FILE"
  echo "| Pyhame executable     : /usr/bin/pyhame"
  echo "| Pyhame libraries      : /usr/lib/pyhame"
  echo "| Help                  : pyhame --help"
  echo "#=================================================================#"
  echo ""
  exit 1
}

remove() {
  clear
  displaytitle "-- Clean"

  if [ -d "/usr/lib/pyhame" ]; then
    displayandexec "Remove Pyhame libraries directorie" rm -fr /usr/lib/pyhame
  fi
  if [ -f "/usr/bin/pyhame" ]; then
    displayandexec "Remove Pyhame" rm -fr /usr/bin/pyhame
  fi

  end_remove
}

end_remove() {
  echo "#=================================================================#"
  echo "| Clean is finished                                               |"
  echo "#=================================================================#"
  echo "| Remove log         : $LOG_FILE"
  echo "| Pyhame             : /usr/bin/pyhame, /usr/lib/pyhame"
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

showMenu () {
  clear
  echo "#=================================================================#"
  echo "|                   -- Pyhame Setup Wizard --                     |"
  echo "#=================================================================#"
  echo "| 1) Installation                                                 |"
  echo "| 2) Remove                                                       |"
  echo "| 3) Quit                                                         |"
  echo "#=================================================================#"
  read -p "Choice : " choice
}
  while [ 1 ]
  do
    showMenu
    case "$choice" in
      "1") installation;;
      "2") remove;;
      "4") exit;;
    esac
  done
