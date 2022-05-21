Cowrie
######

Welcome to this forked Cowrie GitHub repository
*****************************************

* This is a fork of the offical `Cowrie <http://github.com/cowrie/cowrie/>`_ GitHub repository, used for a university project. 

* The main purpose of this fork is to examine the potential of log anonymization.

What is Cowrie
*****************************************

Cowrie is a medium to high interaction SSH and Telnet honeypot
designed to log brute force attacks and the shell interaction
performed by the attacker. In medium interaction mode (shell) it
emulates a UNIX system in Python, in high interaction mode (proxy)
it functions as an SSH and telnet proxy to observe attacker behavior
to another system.

`Cowrie <http://github.com/cowrie/cowrie/>`_ is maintained by Michel Oosterhof.

Documentation
****************************************

The official Documentation can be found `here <https://cowrie.readthedocs.io/en/latest/index.html>`_.

Usage
*****************************************

This fork is intended to be used with Docker, so let's start:

* Build the docker image::

    $ git clone https://github.com/Stinktopf/cowrie.git
    $ cd cowrie
    $ make all docker-build

   
* Start the container::

    $ sudo docker run -d -p 2222:2222 cowrie/cowrie:<VERSION-RETURNED-BY-MAKE>
    
* Access the honeypot::

    $ ssh root@<IP-ADDRESS> -p 2222

* Access the honeypot logs and files by copying the contents of the container to the host-machine::

    $ sudo docker ps
    $ docker cp <CONTAINER-ID>:cowrie/cowrie-git/var/ ${PWD}/logs
    $ cd logs/var
    $ ls

* Stop the container::

    $ sudo docker ps
    $ docker stop <CONTAINER-NAME>

* Configuring Cowrie in Docker

Cowrie in Docker can be configured using environment variables. The
variables start with COWRIE_ then have the section name in capitals,
followed by the stanza in capitals. An example is below to enable
telnet support::

    COWRIE_TELNET_ENABLED=yes

Alternatively, Cowrie in Docker can use an `etc` volume to store
configuration data.  Create `cowrie.cfg` inside the etc volume
with the following contents to enable telnet in your Cowrie Honeypot
in Docker::

    [telnet]
    enabled = yes

Requirements
*****************************************

Software required to run locally:

* Docker
* Make

Files of interest
*****************************************

* `etc/cowrie.cfg` - Cowrie's configuration file. Default values can be found in `etc/cowrie.cfg.dist <https://github.com/cowrie/cowrie/blob/master/etc/cowrie.cfg.dist>`_.
* `share/cowrie/fs.pickle` - fake filesystem
* `etc/userdb.txt` - credentials to access the honeypot
* `honeyfs/ <https://github.com/cowrie/cowrie/tree/master/honeyfs>`_ - file contents for the fake filesystem - feel free to copy a real system here or use `bin/fsctl`
* `honeyfs/etc/issue.net` - pre-login banner
* `honeyfs/etc/motd <https://github.com/cowrie/cowrie/blob/master/honeyfs/etc/issue>`_ - post-login banner
* `var/log/cowrie/cowrie.json` - transaction output in JSON format
* `var/log/cowrie/cowrie.log` - log/debug output
* `var/lib/cowrie/tty/` - session logs, replayable with the `bin/playlog` utility.
* `var/lib/cowrie/downloads/` - files transferred from the attacker to the honeypot are stored here
* `share/cowrie/txtcmds/ <https://github.com/cowrie/cowrie/tree/master/share/cowrie/txtcmds>`_ - file contents for simple fake commands
* `bin/createfs <https://github.com/cowrie/cowrie/blob/master/bin/createfs>`_ - used to create the fake filesystem
* `bin/playlog <https://github.com/cowrie/cowrie/blob/master/bin/playlog>`_ - utility to replay session logs


