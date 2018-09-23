#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil
import re
import json


try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()

except Exception as e:
    print(e)

from django.conf import settings

formsDir = os.path.join(settings.BASE_DIR, 'forms')
resDir = os.path.join(settings.BASE_DIR, 'resources')
viewsDir = os.path.join(settings.BASE_DIR, 'views')
appsDir = os.path.join(settings.BASE_DIR, 'apps')
configFile = os.path.join(settings.BASE_DIR, 'config.json')

def start_new_app(app_name):

    dir_name = os.path.join(appsDir, app_name)
    if os.path.exists(dir_name):
        print("App with the same <{}> name already exists".format(app_name))
        return
    os.mkdir(dir_name)
    print(dir_name)
    temp_path = os.path.join("apps", app_name)
    if app_name.islower():
        execute_django_command(["startapp", app_name.upper(), temp_path])
    elif app_name.isupper():
        execute_django_command(["startapp", app_name.lower(), temp_path])

    for filename in os.listdir(dir_name):
        if filename == "models.py" or filename == "migrations" or filename == "__init__.py":
            pass
        else:
            if os.path.isfile(os.path.join(dir_name, filename)):
                try:
                    os.remove(os.path.join(dir_name, filename))
                    deleted = True
                except Exception as e:
                    print(e)
            else:
                try:
                    shutil.rmtree(os.path.join(dir_name, filename))
                except Exception as e:
                    print(e)

    print("Created app <{}> in apps directory".format(app_name))


def compile_sources(files, cmd=""):
    if not os.path.isfile(configFile):
        print("Missing config.json")
        return
    with open(configFile) as f:
        config = json.load(f)
    binding_list = ["pyqt5", "pyqt4", "pyside", "pyside2"]
    uic_list = ["pyuic5", "pyuic4", "pyside-uic", "pyside2-uic"]
    rcc_list = ["pyrcc5", "pyrcc4", "pyside-rcc", "pyside2-rcc"]
    binding = ""
    uic_path = ""
    rcc_path = ""
    try:
        if config['binding'].lower() in binding_list :
            binding = config['binding'].lower()
        elif len(config['binding']) > 0:
            print("Unknown binding <{}>".format(config['binding']))
            return
        else:
            print("Empty binding in config file!")
            return
    except Exception as e:
        print("Please add field {} in config.json".format(e))
        return
    
    if cmd == "uic":
        try:
            uic_path = config["paths"]["uic"]
            if len(uic_path.strip()) == 0:
                print("Empty uic path in config file, using default <{}> on path".format(uic_list[binding_list.index(binding)]))
                uic_path = uic_list[binding_list.index(binding)]
        except Exception as e:
            print("uic path is not found in config.json, using default <{}> on path".format(uic_list[binding_list.index(binding)]))
            uic_path = uic_list[binding_list.index(binding)]

    
    if cmd == "rcc":   
        try:
            rcc_path = config["paths"]["rcc"]
            if len(rcc_path.strip()) == 0:
                print("Empty rcc path in config file, using default <{}> on path".format(rcc_list[binding_list.index(binding)]))
                rcc_path = rcc_list[binding_list.index(binding)]
        except Exception as e:
            print("uic path is not found in config.json, using default <{}> on path".format(rcc_list[binding_list.index(binding)]))
            rcc_path = rcc_list[binding_list.index(binding)]

    if cmd == "uic":
        command = uic_path
        options = ["--from-imports"]
        extension = ".ui"
        src_dir = formsDir
    elif cmd == "rcc":
        command = rcc_path
        options = []
        extension = ".qrc"
        src_dir = resDir
    original_process_list = []
    original_process_list.append(command)
    for opt in options:
        original_process_list.append(opt)

    ui_files = []
    if len(files) == 0:
        for filename in os.listdir(src_dir):
            if filename.endswith(extension):
                ui_files.append(os.path.join(src_dir, filename))
    else:
        for filename in files:
            path = os.path.join(src_dir, filename)
            if os.path.isfile(path):
                ui_files.append(path)
            else:
                print("File <{}> does not exist, make sure you typed the name correctly".format(filename))
    for filename in ui_files:
        process_list = original_process_list.copy()
        out_name = os.path.splitext(os.path.basename(filename))[0]
        if cmd == "uic":
            out_basename = out_name + '.py'
        elif cmd == "rcc":
            out_basename = out_name + '_rc.py'
        outfile = os.path.join(viewsDir, out_basename)
        process_list.append(filename)
        process_list.append("-o")
        process_list.append(outfile)
        process_prepare = subprocess.Popen(
            process_list, stdout=subprocess.PIPE, universal_newlines=True)
        out, err = process_prepare.communicate()
        if err:
            print(err)
        else:
            if cmd == "uic":
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
            elif cmd == "rcc":
                print("Converting <{}.qrc> to <{}_rc.py> ".format(out_name, out_name))

def migrate_apps(apps, cmd=""):
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

    if cmd == "makemigrations":
        print('Preparing')
        execute_django_command(apps_to_migrate)
    elif cmd == "migrate":
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
    return execute_from_command_line(command)


def deploy():
    hidden_imports = ['http.cookies', 'html.parser',
                      'settings', 'apps', 'django.template.defaulttags',
                      'django.templatetags.i18n', 'django.template.loader_tags',
                      'django.utils.translation'
                      ]
    for app in settings.INSTALLED_APPS:
        if app.startswith('django.'):
            hidden_imports.append(app + '.apps')
        else:
            hidden_imports.append(app)

            cmd = "pyinstaller __main__.py "
    for i in hidden_imports:
        cmd += " --hidden-import "
        cmd += i

    os.system(cmd)
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        dist_dir = os.path.join(os.path.join(settings.BASE_DIR, 'dist'), '__main__')
        if os.path.isdir(dist_dir):
            shutil.copy(settings.DATABASES['default']['NAME'], dist_dir)
    if settings.LANGUAGES is not None:
        for lang in settings.LANGUAGES:
            execute_django_command(["makemessages", "-l", lang[0]])
        execute_django_command(["compilemessages"])
        try:
            shutil.copytree(settings.LOCALE_PATHS[0], os.path.join(dist_dir, '.locale'))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # Parse arguments and make sure they are valid
    if len(sys.argv) < 2:
        execute_django_command(["help"])
        sys.exit()
    command = sys.argv[1]
    if command == "startapp" and len(sys.argv) > 2:
        for app_name in sys.argv[2:]:
            if re.match("^(?![0-9])[a-zA-Z0-9_]*$", app_name):
                start_new_app(app_name)
            else:
                print(
                    "CommandError: '{}' is not a valid app name. Please make sure the name is a valid identifier.".format(
                        app_name))
    elif command == "migrate":
        migrate_apps(sys.argv[2:], cmd=command)
    elif command == "makemigrations":
        migrate_apps(sys.argv[2:], cmd=command)
    elif command == "uic" or command == "rcc":
        compile_sources(sys.argv[2:], cmd=command)
    elif command == "deploy":
        deploy()
    else:
        execute_django_command(sys.argv[1:])


