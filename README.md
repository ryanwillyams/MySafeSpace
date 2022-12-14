# MySafeSpace
*Capstone Project - 2022*


## Summary of Application

The original scope of my project was to create a fast and easy way to set up basic security settings without having to go through different configurations to change them. These settings include and are not limited to: password minimum length requirements, password min/max-age, password complexity, disabling services, removing sudoers/administrators, disabling ssh, and ensuring firewalls are properly set. I decided to add to the project idea to include additional services: automatic backups, system care features, defragmentations, sniffers, anti-virus, and keeping other apps updated.
Having a hub to do paramount security tasks is very handy but I knew this project wouldn’t be capable of doing everything nor ensuring that the user will understand how to properly use all the tools at their disposal. In order to cover these areas, I decided to add a resource section that will provide the user with the latest news in cybersecurity and technology, useful links like haveibeenpwned.com, and additional applications that can do tasks outside of the scope of this project.

## How to run application (Ubuntu 22.04)

- Running with GUI
  - Install PyQt6
    - `sudo pip install PyQt6`
  - Install tabulate
    - `sudo pip install tabulate`
  - Run GUI with app.py
    - `sudo python3 app.py`
  
- Running without GUI (headless)
  - Use terminalUI.py
    - `sudo python3 terminalUI.py`


## Project Outline

**Current Working Implementations**
- Hardening tab
  - Password Requirements
  - Change selected user(s) password
  - Enable/Disable ssh
  - IPTables
- Service tab
- [Website](https://github.com/CodyMang/MySafeSpaceWebsite)
