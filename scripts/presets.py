from os import wait
from scripts.iptables import applyRules
from scripts.passwdReq import (writeToCommon_Password, changeMaxDays,
                              changeMinDays, changeWarnDays)
from scripts.services import (startService, stopService, 
                             enableService, disableService)
from services.systemCare import runSystemCare
# High, medium, and low presets for hardening

# High preset
def highPreset():
    # Change password requirements
    writeToCommon_Password('15', '10', '-1', '-1', '-1', '-1')
    changeMaxDays('180')
    changeMinDays('3')
    changeWarnDays('7')
    # Change services status
    for service in list(open("scripts/servicesHighLvlBlacklist.txt")):
        service = service.rstrip()
        try:
            stopService(service)
            disableService(service)
        except:
            pass
    # Implement IPTables rules
    applyRules()
    # run SystemCare
    runSystemCare()

# Medium preset
def medPreset():
    # Change password requirements
    writeToCommon_Password('15', '10', '-1', '-1', '-1', '-1')
    changeMaxDays('180')
    changeMinDays('3')
    changeWarnDays('7')
    # Change services status
    for service in list(open("scripts/servicesMedLvlBlacklist.txt")):
        service = service.rstrip()
        try:
            stopService(service)
            disableService(service)
        except:
            pass
    for service in list(open("scripts/servicesMedLvlWhitelist.txt")):
        service = service.rstrip()
        try:
            enableService(service)
            startService(service)
        except:
            pass
    # Implement IPTables rules
    applyRules()
    # run SystemCare
    runSystemCare()

# Low preset
def lowPreset():
    # Change password requirements
    writeToCommon_Password('15', '10', '-1', '-1', '-1', '-1')
    changeMaxDays('180')
    changeMinDays('3')
    changeWarnDays('7')
    # Change services status
    for service in list(open("scripts/servicesLowLvlBlacklist.txt")):
        service = service.rstrip()
        try:
            stopService(service)
            disableService(service)
        except:
            pass
    for service in list(open("scripts/servicesLowLvlWhitelist.txt")):
        service = service.rstrip()
        try:
            enableService(service)
            startService(service)
        except:
            pass
    wait()
    # Implement IPTables rules
    applyRules()
    # run SystemCare
    runSystemCare()