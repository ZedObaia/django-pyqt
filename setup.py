#!/usr/bin/env python3
import os
import shutil
import errno


def copy(src, dest):
    try:
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns('setup.py', 'db.sqlite3', '.*', '__pycache__', 'pyqt5-admin'))
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


def main():
    home = os.path.expanduser("~")
    cfg_dir = os.path.join(home, '.pyqt5-django-orm')
    if os.path.exists(cfg_dir):
        shutil.rmtree(cfg_dir)
    src_dir = os.path.abspath('.')

    copy(src_dir, cfg_dir)
    copy('pyqt5-admin', '/usr/bin')
    os.system('chmod +x /usr/bin/pyqt5-admin')


if __name__ == '__main__':
    main()
