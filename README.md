# snek

Demo Game by DaringCuteSeal. I (ezntek) am helping with project setup because she aint know how (i know how to, my friend wanted the code ok)

## running the demo

`path/to/your/python snek`

## development/dependencies

You have to have poetry installed. First, create a virtual environment:

`poetry env use path/to/your/python/interpreter`

if you want a .venv in the folder for better intellisense, then run this command beforehand:

`poetry config virtualenvs.in-project true`

the re-run the command.
After that, `source path/to/your/venv/bin/activate` (`.venv/bin/activate` if you set the in-project setting to true). Then, issue:

`poetry install`

to install the dependencies.
