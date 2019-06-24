#!/usr/bin/env python3
import os
import shutil
import errno
import platform

def copy(src, dest):
    try:
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns('setup.py', 'db.sqlite3', '.*',
         '__pycache__', 'pyqt-admin*', 'build', 'dist', '__main__.spec', 'examples', 'pyqt-admin.exe'))
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


def main():
    home = os.path.expanduser("~")
    cfg_dir = os.path.join(home, '.django-pyqt')
    if os.path.exists(cfg_dir):
        shutil.rmtree(cfg_dir)
    src_dir = os.path.abspath('.')

    copy(src_dir, cfg_dir)
    if platform.system() == 'Linux':
        copy('pyqt-admin', '/usr/bin')
        os.system('chmod +x /usr/bin/pyqt-admin')
    elif platform.system() == 'Darwin' :
        copy('pyqt-admin', '/usr/local/bin/')
        os.system('chmod +x /usr/local/bin/pyqt-admin')
    elif platform.system() == 'Windows':
        path_to_try = [os.path.join(os.environ['WINDIR'], 'system'),
                    os.path.join(os.environ['WINDIR'], 'System'),
                    os.path.join(os.environ['WINDIR'], 'system32'),
                    os.path.join(os.environ['WINDIR'], 'System32')
                    ]
        path = os.environ['PATH'].split(';')
        used_path = ""
        for i in path_to_try:
            if i in path:
                used_path = i
                break
        if len(used_path) == 0:
            print("Please fix PATH environment variable")
            return
        copy('pyqt-admin.exe', used_path)

if __name__ == '__main__':
    main()
