#!/usr/bin/python

################################################################################
# Nagios plugin to check open ports on a server and check if ports are white listed
# Author : Srikrishna Karatalapu
# Version : 1.0
# Date : 10/31/2017
# This is an initial effort to  write a plugin that looks at the open ports on a
# host and verifies is the ports are whitelisted. The whilelisted ports can be
# passed using -l option : allowed ports must be separated by commas
##### ex : check_openPorts.py -l 22,443,8089
# or passed using -c option : config must contain list of allowed ports separated
# by commas
##### ex : check_openPorts.py -c /etc/allowdPorts.txt
# example of the config file configuration
##### cat /etc/allowdPorts.txt
##### 11491,12858,12866,15134,15199
################################################################################
import commands,sys
from optparse import OptionParser


class Ports:


    def __init__(self):
	     pass

    # Method to define commandline options for the plugin
    def handleCmdLine(self):
        """
        Parse the command line arguments and set the appropriate
        member variables of self.  Returns true upon success, false
        otherwise
        """
        description = "Nagios monitoring script for virt host\n"
        usage = ("%prog <options>\n")
        parser = OptionParser(usage=usage, description=description)

        parser.add_option("-c", "--config",
                          type="string",
                          help="path to open ports configuration file")
        parser.add_option("-l", "--list",
                          type="string",
                          help="supply list of allowed ports seperated by comma.")

        (self.options, args) = parser.parse_args()

    # Method to check if the user has read permissions on the config file passed
    # through the command line argument
    def fileCheck(self,fileName):
        try:
          open(fileName, "r")
          return 0
        except IOError:
          print "Error: File does not appear to exist."
          sys.exit(1)

    # Method to check the if the command being executed is valid or not
    def cmdCheck(self,cmd):
        if commands.getstatusoutput(cmd)[0] != 0:
            print "Invalid command, Please check to see if the command is correct !!!"
            sys.exit(1)

    # Method gets the list of allowed ports passed using the command line argument(-l)
    # or through the config file passed using the -c option.
    def whiteList(self):
        self.handleCmdLine()
        allowedPorts = ''
        if self.options.list is not None:
            allowedPorts = list(set(self.options.list.split(',')))
            allowedPorts.sort(key=int)

        if self.options.config is not None:
            if self.fileCheck(self.options.config) == 0:
                configFile = open(self.options.config ,'r')
                allowedPorts = list(set(configFile.read().rstrip().split(',')))
                configFile.close()
                allowedPorts.sort(key=int)

        if self.options.config is None and self.options.list is None :
            print "Invalid argument.\nPlease run the plugin with "\
                    "valid argument. Please use the --help option "\
                    "to find the list of valid arguments."
            sys.exit(1)

        return allowedPorts

    # Method Runs netstat get the list of open ports
    def listeningPorts(self):
        self.cmdCheck('netstat --listen | grep LISTENING')
        ports = commands.getoutput('netstat --listen | grep LISTENING ')
        openPorts = []
        for port in ports.split('\n'):
            if port.split()[7] not in openPorts:
               openPorts.append(port.split()[7])
        openPorts.sort(key=int)
        return openPorts


    # Method to print the output messsage with the appropriate exit status
    def alertMessage(self,message, exitStatus):
        print message
        sys.exit(exitStatus)

    # Method to set alert level depending on passed status codes
    # List bad ports as bad listeners along with all the open ports on the server.
    def portCheck(self, alert, openPorts, badPorts):

        if alert == 'GREEN':
            message = "OK - No bad listeners.\nOpen ports %s"\
                                         %(','.join(openPorts))
            exitStatus = 0

        elif alert == 'RED':
            message = "CRITICAL - bad listeners found %s.\nOpen ports %s"\
                                    %(','.join(badPorts),','.join(openPorts))
            exitStatus = 2

        self.alertMessage(message,exitStatus)

    # Method that gets list of open and allowedPorts from listeningPorts and whiteList
    # Sets alert to GREEN is diff is empty else to RED.
    def run(self):
        alert  = ''
        openPorts  = self.listeningPorts()
        allowedPorts = self.whiteList()
        badPorts = set(openPorts) - set(allowedPorts)
        if len(badPorts) == 0:
            alert = 'GREEN'
        else :
            alert ='RED'

        self.portCheck(alert, openPorts, badPorts)

if __name__ == "__main__":
    plugin = Ports()
    plugin.run()
