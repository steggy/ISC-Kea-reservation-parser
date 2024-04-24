# ISC-Kea reservation parser

menu driven terminal script to manage kea-dhcp4.conf file.

## Description

To avoid human error, this script was created to manage the json config file for kea dhcp.
Including Dup checking and formatting of hostname, IP, mac.
When saving a record the original file will not be overwritten. A new file will be created with the name "pipe-kea-dhcp4.conf" to be used with pipeline
If multiple saves are complete the saved file will be incremented, not destroying history.  

## Getting Started

### Dependencies

Python3
tabulate

### Installing

Clone the repo
Adjust the default setting in parse.conf file


### Executing program

Call parse-reserve.py with the file to edit.
The file must be in the kea-dhcp4.conf format
```
./parse-reserve.py file.conf
```

``

## Authors

Steggy
steggy@gmail.com


## Version History

* 0.1
    * Initial Release to Github


