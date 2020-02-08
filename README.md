
# Project : Developing Python Scripts (modules of Ansible) to automate a vulnerability scanner (Rapid7 Nexpose).


*Python Code Design*

This project has 3 Python scrips which work separately following:

•	nexpose01_start_scan.py

This Python scrip intends for user to specify the IP address of asset or target which will be scanned vulnerabilities.

•	nexpose02_show_assets.py

This script will show details of assets (IP address, hostname, and ID number) in the Nexpose system including assets which have been scanned or asset which is being scanned.

•	nexpose03_show_vulnerabilities.py

User has to assig the ID of asset, then this script will show details of vulnerabilities 


(PS: Python has hard-code of username and password)
