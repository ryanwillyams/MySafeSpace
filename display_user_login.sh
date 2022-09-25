# This file had to be written in shell since certain commands require the use of 
# of the # command in shell and python is forced to use that as a comment

# Remove the # from the command that is to be changed 
sed -i 's/# disable-user-list=false/disable-user-list=false/' /etc/gdm3/greeter.dconf-defaults

echo "------------------------------------"
echo "Options"
echo "------------------------------------"
echo "1. Display the last User "
echo "2. Do not display the last User "
echo "0. Back"
echo "------------------------------------"
echo -n "Select an option: " 
read INPUT
echo "------------------------------------"


case "$INPUT" in
    "1") echo "The last logged in User name will still show when loggin in"
         sed -i 's/disable-user-list=true/disable-user-list=false/' /etc/gdm3/greeter.dconf-defaults
    break;;
    "2") echo "The last logged in User name will not show when loggin in"
         sed -i 's/disable-user-list=false/disable-user-list=true/' /etc/gdm3/greeter.dconf-defaults 
    break;;
    "0") echo "Back to main menu."
    break;;
    *) echo "Invalid entry."
    ;;
esac
