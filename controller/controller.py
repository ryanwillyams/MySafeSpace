import scripts as sc
import services as sv
from enum import Enum

B_MODE = Enum('Backup_Modes', 'MANUAL LOCAL REMOTE')

# class Scripts:
# changePass(pword, uList) 
#   pword - str representing password to replace current
#   uList - list of users to apply change to
#
#   description - changes passwords for selected list of users
#
#   example call: controller.changePass(pword, uList)
#
def changePass(pword: str, uList: list) -> None:
    try:
        if isinstance(uList, list) and isinstance(pword, str):
            sc.change_passwds.passwdChange(pword, uList)
        else:
            raise TypeError
    except TypeError:
        print('ControllerException: TypeError in call to '
            + 'controller.changePass(pword: str, uList: list)')

    pass

# passwordRequirements(...)
#   maxdays     - int representing max days before changing password
#   mindays     - int represeting min days before changing password
#   warning     - int representing num of days before recieving notification
#   minlen      - int representing min passord length
#   numPassMem  - int representing number of previous passwords to remember
#   upper       - bool to set upper case requirement
#   lower       - bool to set lower case requirement
#   digits      - bool to set digit requirement
#   special     - bool to set special character requirement
#   
#   description - this controller condenses the passwdReq calls into 
#       one simple function and attempts to catch any exceptions thrown.
#
def passwordRequirements(maxdays: int, mindays: int, warning: int
    ,  minlen: int, numPassMem: int
    , upper: bool, lower: bool, digits: bool, special: bool) -> None:
    try: 
        sc.passwdReq.changeMaxDays(maxdays)
        sc.passwdReq.changeMinDays(mindays)
        sc.passwdReq.changeWarnDays(warning)
        sc.passwdReq.writeToCommon_Password(minlen, numPassMem, upper
            , lower, digits, special)
    except Exception:
        print('ControllerException: passwordRequirments()')

    pass
# changeSudoers(uList)
#   uList - list representing list of user(s) to add/remove from sudo privilages
#   
#   description - changes user sudo privilages
#
def changeSudoers(uList: list, addFlag: bool) -> None:
    try:
        if addFlag == True:
            sc.sudo_priv.addSudo(uList)
        else:
            sc.sudo_priv.removeSudo(uList)
    except Exception:
        print(Exception)

    pass

#
# 
# 
#
def services() -> None:
    pass

# class Services:

# getUpdates() -> None
# 
#   description - fetches updates for all programs/drivers and installs
#
def getUpdates() -> None:
    sv.getUpdates.update()
    
    pass


# automaticBackups() -> str
#   ? -
# 
#   description - schedule automatic backup on user desired interval, 
#   back up manually, local, or remote
# 
#   example calls:  automaticBackups('MANUAL', None )
#                   automaticBackups('INTERVAL', 90) # not implemented yet
# 
def automaticBackups(option: B_MODE, intervalDays: int) -> str:
    try:
        match option:
            case B_MODE.MANUAL.name:
                sv.automaticBackup.manual_backup()
            case B_MODE.LOCAL.name:
                sv.automaticBackup.local_backup()
            case B_MODE.REMOTE.name:
                sv.automaticBackup.remote_backup()
            case _:
                #setInterval maybe? idk yet doesn't look implemented
                pass
    except Exception:
        print(Exception)

    pass