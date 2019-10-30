# Nagios Plugin

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Nagios plugin repo contains to scripts used by the nagios agents to run for cpu load and open ports on a host.

* _**Check_load.py**_ : checks if the 1,5 and 15 minute load is greater than the threshold which is the available cpu's on the system.
* _**check_openPorts.py**_: checks if the whitelisted port are the only ports currently open.

### Installation

 Follow the below steps for installation

```sh
	$ git clone https://github.com/SriKaratalapu/Nagios-plugins.git
	$ cd nagios-plugins
	$ cp ./* /usr/local/nagios/libexec/
```

### How To Use check_load.py:
To monitor remote Linux server:
1. Keep the plugin in /usr/local/nagios/libexec directory.
2. Add following line to the nrpe.cfg file:
    ```sh
    command[check_load]=sudo /usr/local/nagios/libexec/check_load.py
    ```
3. Add the following line to /etc/sudoers file:
    ```sh
    nagios ALL=(ALL) NOPASSWD:/usr/local/nagios/libexec/check_load.py
    ```

### How To Use check_load.py:
To monitor remote Linux server:
1. Keep the plugin in /usr/local/nagios/libexec directory.
2. Add following line to the nrpe.cfg file,  The whilelisted ports can be passed using -l option
    ```sh
    command[check_openPorts]=sudo /usr/local/nagios/libexec/check_openPorts.py -l 22,443,8089
    ```
    **OR**
    passed using -c option : config must contain list of allowed ports separated by commas
    ```sh
    command[check_openPorts]=sudo /usr/local/nagios/libexec/check_openPorts.py -c /etc/allowdPorts.txt
    ```

3. Add the following line to /etc/sudoers file:
    ```sh
    nagios ALL=(ALL) NOPASSWD:/usr/local/nagios/libexec/check_openPorts.py
    ```

### Contributing
To contribute please follow the below steps
1. Fork it.
2. Create your feature branch (git checkout -b $branch-name).
3. Commit your changes (git commit -am 'Fixed blah').
4. Push to the branch (git push origin fixing-blah).
6. Create a new pull request.
_**Do not update changelog or attempt to change version.**_
