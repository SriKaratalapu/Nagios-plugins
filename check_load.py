#!/usr/bin/python

################################################################################
# Nagios plugin to check load
# Author : Srikrishna Karatalapu
# Version : 1.0
# Date : 10/27/2017
# This is an initial effort to  write a plugin that looks at the no. cores on
# the host to set the CRITCAL, WARNING and OK thresholds
################################################################################
import commands,sys

class Load:

    def __init__(self):
	pass

    # Method to check the if the command being executed is valid or not
    def cmdCheck(self,cmd):
        if commands.getstatusoutput(cmd)[0] != 0:
            print "Invalid command, Please check to see if the command is correct !!!"
            sys.exit(1)

    # Method Runs uptime to reurn 3 load average values
    def loadAverage(self):
        self.cmdCheck('uptime')
        return  commands.getoutput('uptime').split()[-3:]

    # Method Runs nproc to get the no. of cpu's to set the alert threshold
    def cpuCount(self):
        self.cmdCheck('nproc --all')
        return  commands.getoutput('nproc --all')

    # Method to print the output messsage with the appropriate exit status
    def loadMessage(self,message, exitStatus):
        print message
        sys.exit(exitStatus)

    # Method to set alert level depending on passed status codes
    def loadCheck(self, alert, loadInfo, threshold):

        if alert == 'GREEN':
            message = "OK - cpu load less than no. of allocated cpus(%s).\n%s"\
                                                        %(threshold,loadInfo)
            exitStatus = 0

        elif alert == 'YELLOW':
            message = "WARNING - cpu load equal to no. of allocated cpus(%s).\n%s"\
                                                        %(threshold,loadInfo)
            exitStatus = 1

        elif alert == 'RED':
            message = "CRITICAL - cpu load greater than the no. of allocated cpus(%s).\n%s"\
                                                        %(threshold,loadInfo)
            exitStatus = 2

        self.loadMessage(message,exitStatus)

    # Method that gets values from loadAvergae and cpuCount to check
    # if load is OK, CRICTICAL or at WARNING level
    def run(self):
        alert  = 'GREEN'
        loads  = self.loadAverage()
        threshold = int(self.cpuCount())

        current_load = float(loads[0].replace(',',''))
        five_minute_load = float(loads[1].replace(',',''))
        fifteen_minute_load = float(loads[2].replace(',',''))

        loadInfo = "curent_load=%sfive_minute_average=%sfifteen_minute_average=%s"\
                    %(loads[0],loads[1],loads[2])
        loadInfo += '|' + loadInfo.replace(',',';')

        if current_load == threshold or \
            five_minute_load == threshold or \
            fifteen_minute_load == threshold:

            alert = 'YELLOW'

        elif current_load > threshold or \
            five_minute_load > threshold or \
            fifteen_minute_load > threshold:
            alert ='RED'

        self.loadCheck(alert, loadInfo, threshold)

if __name__ == "__main__":
    plugin = Load()
    plugin.run()
