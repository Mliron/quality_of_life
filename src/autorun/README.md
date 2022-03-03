# Autorun script
This script watches targeted files and runs a command every time when any of the files have been updated.<br/>
Makefile contains rules to make this script accessible from anywhere (user-bound). Run `make` or `make help` to get more information.

## Details
Script checks if any targeted file timestamp has changed. If it has, it executes the first given file by default. This behaviour can be changed with the `-c` option when starting the script.

## Examples
`auto_run.py main.c` - Compiles `main.c` and executes the compiled code<br/>
`auto_run.py main.c lib0.c` - Compiles `main.c` and executes the compiled code every time any of targeted files are updated<br/>
`auto_run.py main.py module0.py` - Runs `main.py`script every time any of targeted files are updated<br/>
`auto_run.py -l python main.code` - Executes `main.code` as a python script<br/>
`auto_run.py -c "make run" main.c lib0.c lib1.c` - Runs `make run` every time any of targeted files are updated<br/>

## Plans for the future
Probably nothing, I am qutie happy with this script.<br/>
Maybe add comments to make it readable
