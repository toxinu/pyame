#!/bin/sh
script_version="0.1"

# Globals variables
#-----------------------------------------------------------------------------
DATE=`date +"%Y%m%d%H%M%S"`
LOG_FILE="/tmp/pyhame-remove-$DATE.log"

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

remove() {
  if [ -d "/usr/lib/pyhame" ]; then
    displayandexec "Remove Pyhame libraries directorie" rm -fr /usr/lib/pyhame
  fi
  if [ -f "/usr/bin/pyhame" ]; then
    displayandexec "Remove Pyhame" rm -fr /usr/bin/pyhame
  fi
  if [ ! -z "ls /usr/lib/python3.2/site-packages/ | grep '^[jJ]inja*'" ]; then
    displayandexec "Remove Jinja2" rm -fr /usr/lib/python3.2/site-packages/{jinja2*,Jinja*}
  fi
}

end() {
  echo ""
  echo "=============================================================================="
  echo "Clean is finished"
  echo "=============================================================================="
  echo "Log for the remove script   : $LOG_FILE"
  echo "Removed pyhame folders      : /usr/bin/pyhame, /usr/lib/pyhame"
  echo "Removed jinja2 folders      : /usr/lib/python3.2/site-packages/{jina2*,Jinja*}"
  echo "=============================================================================="
  echo ""
}

# Check if root user is used
if [ "$(id -u)" != "0" ]; then
  echo "This script should be run as root."
  echo "Syntaxe: sudo $0"
  exit 1
fi

displaytitle "-- Clean"
remove
end
