
# Project : Developing Python Scripts (modules of Ansible) to automate a vulnerability scanner (Rapid7 Nexpose).

This project is a part of studying at Kingston University, London.

# *Python Code Design (in Library folder)*

This project has 3 Python scrips which work separately following:

•	nexpose01_start_scan.py

This Python scrip intends for user to specify the IP address of asset or target which will be scanned vulnerabilities.

•	nexpose02_show_assets.py

This script will show details of assets (IP address, hostname, and ID number) in the Nexpose system including assets which have been scanned or asset which is being scanned.

•	nexpose03_show_vulnerabilities.py

User has to assig the ID of asset, then this script will show details of vulnerabilities 


(PS: Python has hard-code of username and password)

# *Running (at YAML files)*

Running software of this project has a few steps which is in accordance with the Ansible way. In order to run by Ansible, YAML files, which is likely the procedure file, will be run via command line that firstly, “nexpose01_start_scan.py” will be run, then “nexpose02_show_assets.yaml”, and finally, “nexpose03_show_vulnerabilities.yaml” will be run.
