# django-pyqt
This is a tool to help you develop desktop applications using Python Qt bindings of your choice for the 'front end' with django ORM for the backend.

 Currently we only support *nix.

Tested with PyQt5.11 and Django 2.1 on Ubuntu 18.4

Note that you need PyQt5 and Django to be already installed
***

# Installation
>Clone the repo then run:
`sudo ./setup.py`

## Usage
##### Start new project using

`pyqt-admin --startproject proj_name destination`


Project Structure:

```.
├── apps  -> where django apps go
├── forms -> where Qt *.ui files go
├── resources -> where Qt *.qrc files and assets(images, fonts, ...) go
├── viewManagers -> your views controllers go here
├── views -> where pyuic5 & pyrcc5 generated *.py files go
├── __main__.py -> start point for your application
├── manage.py
├── settings.py
├── config.json
```
***
Edit  `config.json` to change the binding i.e (PyQt4, PyQt4, PySide or PySide2)
PyQt5 by default.

set `django` to `false` to only use qt with the same commands.

Edit `hidden-imports` to add imports for pyinstaller
***

#### Django Commands
##### Create a new django app inside the apps directory

`python3 manage.py startapp appname appname2 `

##### Add appName to INSTALLED_APPS in settings.py

`INSTALLED_APPS = ["apps.appname",]`

##### To prepare models migrations 
`python3 manage.py makemigrations [app1, app2, ...]`

##### To migrate your models
`python3 manage.py migrate [appname, appname2, ...]`

Note that leaving apps blank will try to migrate all apps

##### To use other django manage.py commands
`python3 manage.py commandm`

***
#### Qt Commands

##### Convert `*.ui` files to `.py` files using `uic` command

`python3 manage.py uic [file1.ui, file2.ui]`

Note that leaving files blank will compile all UI files inside forms directory

##### Convert `*.qrc` files to `.py` files using `rcc` 

`python3 manage.py rcc [file1.ui, file2.ui]`

#### Using Pyinstaller
`python3 manage.py deploy`



#### Start coding !
Now you can start using django (models, authentication, ... ) inside your application

***
### Known Issues

<ul>
    <li>PyInstaller deployment is not fully implemented yet</li>
</ul>

### TODO

<ul>
    <li>Add support for windows</li>
    <li>fix pyinstaller issues</li>
    <li>create a vscode package</li>
    <li>create a pip package</li>
</ul>
