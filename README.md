# pyqt5-django-orm
Starter project and directory structure to use PyQt5 with Django ORM

## Usage

`python3 pyqtmgr.py -c`

>To compile `*.ui` files to `.py` files using `pyuic5`

`python3 pyqtmgr.py --startapp appName`

>Creates a new django app inside the apps directory with models file only

Add appName to INSTALLED_APPS in settings.py

`INSTALLED_APPS = ["apps.appName",]`


Now you can start using your model inside your main application