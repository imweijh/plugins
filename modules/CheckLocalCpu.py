#!/usr/bin/env python

# check_local_cpu.py - Copyright (C) 2012 Matthieu FOURNET, fournet.matthieu@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

######################################### CheckLocalCpu.py ##########################################
# MODULE PART
#
# VERSION :     20121104
########################################## ##########################################################

import NagiosPlugin
import psutil


class CheckLocalCpu(NagiosPlugin.NagiosPlugin):


    def getCpuUsagePercent(self):
        self.cpuUsagePercent = psutil.cpu_percent(interval=1)
        self._objDebug.show(self.cpuUsagePercent)
       


    """
    def getCpuTimes(self):
        # help with named tuples :
        # http://stackoverflow.com/questions/2970608/what-are-named-tuples-in-python
        # http://pysnippet.blogspot.fr/2010/01/named-tuple.html
        self._cpuTimes  = psutil.cpu_times()
        self._cpuData   = {}
#        print self._cpuTimes.user
        self._fields    = ['user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq']
        self._totalTime = 0
        for fieldName in self._fields:
#            print fieldName
            self._cpuData[fieldName] = {}
            time = getattr(self._cpuTimes, fieldName)
            self._cpuData[fieldName]['cpuTime'] = time
            self._totalTime += time
#        print self._cpuData





    def computeCpuUsagePercent(self):
        debugTotalPercents  = 0
        debugCpuUsages      = ''

        self._cpuData['totalWithoutIdle'] = {'cpuPercent': 0}
        for fieldName in self._fields:
            self._cpuData[fieldName]['cpuPercent'] = self._objUtility.computePercentage(self._cpuData[fieldName]['cpuTime'], self._totalTime)
            debugCpuUsages += fieldName + ' : ' + `self._cpuData[fieldName]['cpuPercent']` + ' %' + '\n'
            debugTotalPercents += self._cpuData[fieldName]['cpuPercent']
            if fieldName != 'idle':
                self._cpuData['totalWithoutIdle']['cpuPercent'] += self._cpuData[fieldName]['cpuPercent'] 

        # DEBUG
#        self._objDebug.show(self._cpuData)
#        self._objDebug.show('CPU USAGES : ' + debugCpuUsages)
#        self._objDebug.show('total percents               = ' + `debugTotalPercents` + '%' \
#            "\n              total percents (except idle) = " + `self._cpuData['totalWithoutIdle']['cpuPercent']` + '%')
        # /DEBUG
        self.cpuUsagePercent = round(self._cpuData['totalWithoutIdle']['cpuPercent'], self._decimalPlaces)
    """

        
    def computeExitCode(self, warningThreshold, criticalThreshold):
        """
        Compare the 'totalWithoutIdle' CPU time VS the warn / crit thresholds
        and return the corresponding exit code.
        """
        # /!\ Thresholds are internally known as strings
        warningThreshold    = int(warningThreshold)
        criticalThreshold   = int(criticalThreshold)

#        cpuUsage            = self._cpuData['totalWithoutIdle']['cpuPercent']
        self._exitCode      = None

        if(self.cpuUsagePercent < warningThreshold):
            self._exitStatus = 'OK'
        elif(self.cpuUsagePercent > criticalThreshold):
            self._exitStatus = 'CRITICAL'
        else:
            self._exitStatus = 'WARNING'

        self._exitCode = self._exitCodes[self._exitStatus]

        self._objDebug.show('CPU usage : ' + `self.cpuUsagePercent` + '%' \
            + "\nWarning threshold : " + str(warningThreshold) \
            + "\nCritical threshold : " + str(criticalThreshold) \
            + "\nExit code : " + str(self._exitCode) \
            + "\nExit status : " + self._exitStatus
            )
