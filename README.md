# Python GUI 
An exercise for python gui

## On Ubuntu 24.04
PEP668 recommand that pip package should be installed in a virtual environments. We need to proceed as following:

`python3 -m venv ~/.venv/[Package name]`

then use the command

`~/.venv/[Package name]/bin/pip install [package name]`

then add the virtual environement to the path:

`export PATH=$HOME/.venv/[Package name]/bin:$PATH`
