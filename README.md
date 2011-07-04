# Description

__Pyhame 0.3__ is an easy website creator written in _Python_.
You just put files/folders in your content folder and launch pyhame.
You dont need to do Html/Css/Php or other web language.

## Where is the magic ?

After that your files/folders will be automaticaly parse and a static html5 website will be create with a embed http python server.

__Good things for simple users :__

  - Just write text files
  - __Markdown__ usage
  - Just create directories
  - Just run pyhame.py
  - Embedded Http Web Server
  - Downloadable file link
  - Permalink on each page
  - Simple Html template
  - Very light static web site
  - W3C Html5 validate ([link](http://validator.w3.org/check?uri=http%3A%2F%2Fsocketubs.net%2F))
  - Create an .zip archive of your website on each html rendering
  - Write with the best editor ever vim through ssh (for bearded man)		

__Others good things for advanced users :__

  - Easy to write template
  - Choose between ipv4 and ipv6
  - Python 3.x
  - Sweet update script with git repo (just for Linux and Mac Os with git-core)
  - Coded with my feet

## Preview

Just create a tree files/directories like that :

![alt text](http://mail.socketubs.net/tree_screen.png "Tree files")

You can easy watch the face of default template on my [website](http://socketubs.net).

In just one command. Easy to understand the simple usage of __pyhame__.

## Compatibily

  - Linux (tested on archlinux and Debian Squeeze with [python3.1-minimal](http://packages.debian.org/squeeze/python3.1-minimal))
  - Windows (tested on Windows Seven 64bits with [Python 3.2 x86-64](http://www.python.org/download/releases/3.2/)
  - Mac Os (not tested)

## Versions

  - 0.3 : _July 4 2011_

# Help

## Installation

Nothing to do, just the python package.
Debian :
	apt-get install python3.1-minimal
Archlinux :
	pacman -S python

## Run

Debian :
	apt-get install screen
	screen -S pyhame
	python3 pyhame.py # And Ctrl-A + D
	screen -x pyhame # To attach the pyhame screen
Archlinux :
	pacman -S screen
	screen -S pyhame
	./pyhame.py # And Ctrl-A + D
	screen -x pyhame # To attach the pyhame screen

## Web proxy

Nginx :
	server {
    	listen   80;
	    server_name wiki.socketubs.net www.socketubs.net socketubs.net;
	
    	access_log  /var/log/nginx/socketubs.net.access.log;
	    error_log /var/log/nginx/socketubs.net.error.log;
	
	    location / {
	        proxy_pass http://localhost:8000/;
	    }
	}

## Write content

Just use your favorite editor and markdown syntax.
Many editors works with Markdown, sometimes with plugin.

For all plateform and for people who want to have a live preview : [Showdown](http://softwaremaniacs.org/playground/showdown-highlight/).
