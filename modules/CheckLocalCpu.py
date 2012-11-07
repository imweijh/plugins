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


    def computeExitCode(self, warningThreshold, criticalThreshold):
        """
        Compare the 'totalWithoutIdle' CPU time VS the warn / crit thresholds
        and return the corresponding exit code.
        """
        # /!\ Thresholds are internally known as strings
        warningThreshold    = int(warningThreshold)
        criticalThreshold   = int(criticalThreshold)

#        self._exitCode      = None
        exitCode      = None

        if(self.cpuUsagePercent < warningThreshold):
            self._exitStatus = 'OK'
        elif(self.cpuUsagePercent > criticalThreshold):
            self._exitStatus = 'CRITICAL'
        else:
            self._exitStatus = 'WARNING'

#        self._exitCode = self._exitCodes[self._exitStatus]
        exitCode = self._exitCodes[self._exitStatus]

        self._objDebug.show('CPU usage : ' + `self.cpuUsagePercent` + '%' \
            + "\nWarning threshold : " + str(warningThreshold) \
            + "\nCritical threshold : " + str(criticalThreshold) \
#            + "\nExit code : " + str(self._exitCode) \
            + "\nExit code : " + str(exitCode) \
            + "\nExit status : " + self._exitStatus
            )
        return exitCode


    def computeExitStatus(self, warningThreshold, criticalThreshold):
        """
        Compare the 'totalWithoutIdle' CPU time VS the warn / crit thresholds
        and return the corresponding exit code.
        """
        # /!\ Thresholds are internally known as strings
        warningThreshold    = int(warningThreshold)
        criticalThreshold   = int(criticalThreshold)

        exitStatus = ''

        if(self.cpuUsagePercent < warningThreshold):
            exitStatus = 'OK'
        elif(self.cpuUsagePercent > criticalThreshold):
            exitStatus = 'CRITICAL'
        else:
            exitStatus = 'WARNING'

        """
        exitStatus = self._exitCodes[self._exitStatus]

        self._objDebug.show('CPU usage : ' + `self.cpuUsagePercent` + '%' \
            + "\nWarning threshold : " + str(warningThreshold) \
            + "\nCritical threshold : " + str(criticalThreshold) \
#            + "\nExit code : " + str(exitCode) \
            + "\nExit status : " + self._exitStatus
            )
        """
        return exitStatus
