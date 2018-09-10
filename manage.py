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


def start_new_app(app_name):
    dir_name = os.path.join(appsDir, app_name)
    if os.path.exists(dir_name):
        print("App with the same <{}> name already exists".format(app_name))
        return
    os.mkdir(dir_name)
    models_file = os.path.join(dir_name, 'models.py')
    init_file = os.path.join(dir_name, '__init__.py')
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
    print("Created app <{}> in apps directory".format(app_name))


def compile_sources(files):
    ui_files = []
    if len(files) == 0:
        for filename in os.listdir(formsDir):
            if filename.endswith(".ui"):
                ui_files.append(os.path.join(formsDir, filename))
    else:
        for filename in files:
            path = os.path.join(formsDir, filename)
            if os.path.isfile(path):
                ui_files.append(path)
            else :
                print("UI File <{}> does not exist, make sure you typed the name correctly".format(filename))
    for filename in ui_files:
        out_name = os.path.splitext(os.path.basename(filename))[0]
        out_basename = out_name + '.py'
        outfile = os.path.join(viewsDir, out_basename)
        process_prepare = subprocess.Popen(
            ["pyuic5", filename, '-o', outfile], stdout=subprocess.PIPE, universal_newlines=True)
        out, err = process_prepare.communicate()
        if err:
            print(err)
        else:
            print("Converting <{}.ui> to <{}.py> ".format(out_name, out_name))
            views_init = os.path.join(viewsDir, '__init__.py')
            f = open(views_init, 'r')
            lines = f.readlines()
            f.close()
            f = open(views_init, 'a')
            line = 'from . import {}\n'.format(out_name)
            if line not in lines:
                f.write(line)
                f.write('\n')
            f.close()


def migrate_apps(apps):
    apps_to_migrate = ["makemigrations"]
    if len(apps) == 0:
        # Migrate all apps
        for app in os.listdir(appsDir):
            if os.path.isdir(os.path.join(appsDir, app)):
                if app == "__pycache__":
                    pass
                else:
                    apps_to_migrate.append(app)
    else:
        for app in apps:
            if os.path.isdir(os.path.join(appsDir, app)):
                apps_to_migrate.append(app)
            else:
                print("App <{}> does not exist, make sure you typed the name correctly".format(app))
                print('')

    print('Preparing')
    execute_django_command(apps_to_migrate)
    print("Migrating")
    execute_django_command(['migrate'])


def execute_django_command(cmd):
    command = ['manage.py']
    command.extend(cmd)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(command)


if __name__ == '__main__':
    # Parse arguments and make sure they are valid
    ap = argparse.ArgumentParser()
    ap.add_argument("--uic", help="compile ui forms", nargs='*', action="store", dest="uic")
    ap.add_argument("-s", "--startapp", help="start new app", nargs='*', action="store", dest="startapp")
    ap.add_argument("-m", '--migrate', help='Migrate apps', nargs='*', action="store", dest="migrate")
    ap.add_argument("-d", "--django", help="Run Django command", nargs='*', action="store", dest="django")

    args = vars(ap.parse_args())
    if args['startapp'] is not None:
        for app in args['startapp']:
            start_new_app(app)
    if args['uic'] is not None:
        compile_sources(args['uic'])
    if args['migrate'] is not None:
        migrate_apps(args['migrate'])
    if args["django"] is not None:
        execute_django_command(args["django"])



