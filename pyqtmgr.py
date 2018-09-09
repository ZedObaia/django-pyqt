#!/usr/bin/env python3
import os
import subprocess
import argparse
try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

except Exception as e:
    print(e)

from django.conf import settings
formsDir = os.path.join(settings.BASE_DIR, 'forms')
viewsDir = os.path.join(settings.BASE_DIR, 'views')
appsDir = os.path.join(settings.BASE_DIR, 'apps')


def start_new_app(appname):
    dirname = os.path.join(appsDir, appname)
    if os.path.exists(dirname):
        print("App with the same name already exists")
        return
    os.mkdir(dirname)
    models_file = os.path.join(dirname, 'models.py')
    init_file = os.path.join(dirname, '__init__.py')
    if not os.path.exists(init_file):
        f = open(init_file, 'w')
        f.close()
    if not os.path.exists(models_file):
        f = open(models_file, 'w')
        f.write('''import sys
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Make sure you have django installed")
    sys.exit()

# Your models go here
# class User(models.Model):
#     username = models.CharField(max_length=255)
''')
        f.close()


def compile_sources():
    uifiles = []
    for filename in os.listdir(formsDir):
        if filename.endswith(".ui"):
            uifiles.append(os.path.join(formsDir, filename))
    for filename in uifiles:
        out_name = os.path.splitext(os.path.basename(filename))[0]
        out_basename = out_name + '.py'
        outfile = os.path.join(viewsDir, out_basename)
        process_prepare = subprocess.Popen(
            ["pyuic5", filename, '-o', outfile], stdout=subprocess.PIPE, universal_newlines=True)
        out, err = process_prepare.communicate()
        if err:
            print(err)
        else:
            views_init = os.path.join(viewsDir, '__init__.py')
            f = open(views_init, 'r')
            lines = f.readlines()
            f.close()
            f = open(views_init, 'a')
            line = 'from . import {}\n'.format(out_name)
            if not line in lines:
                f.write(line)
                f.write('\n')
            f.close()


if __name__ == '__main__':
    # Parse arguments and make sure they are valid
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', "--startapp", nargs=1, required=False, help="start new app")
    ap.add_argument('-c', "--compile", action='store_true', required=False, help="compile ui forms")

    args = vars(ap.parse_args())

    if args['startapp']:
        start_new_app(args['startapp'][0])

    elif args['compile']:
        compile_sources()

    else:
        ap.exit(ap.print_help())

