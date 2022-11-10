from scripts.passwdReq import (writeToCommon_Password, changeMaxDays,
                              changeMinDays, changeWarnDays)
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
    # run SystemCare
    runSystemCare()
    pass

# Medium preset
def medPreset():
    # Change password requirements
    writeToCommon_Password('15', '10', '-1', '-1', '-1', '-1')
    changeMaxDays('180')
    changeMinDays('3')
    changeWarnDays('7')
    # Change services status
    # run SystemCare
    pass

# Low preset
def lowPreset():
    # Change password requirements
    writeToCommon_Password('15', '10', '-1', '-1', '-1', '-1')
    changeMaxDays('180')
    changeMinDays('3')
    changeWarnDays('7')
    # Change services status
    # run SystemCare
    pass