import os
from fabric.api import cd, env, run, get, local
from fabric.colors import blue, green, red
from fabric.tasks import Task


class RemoteTask(Task):
    settings = {
        'install_requirements': True,
        'collect_static': True,
        'syncb_migrate': True,
        'resetsh': False,
        'compilejsi18n': False,
        'branch': 'origin master',
        'use_src': False,
        'less2css': False,
        'location_less': 'project/static/project/css/style.less',
        'location_css': 'project/static/project/css/style.css',
        'is_django_17_or_higher': False,
        'requirements_location': 'requirements.txt',
    }
    local_settings = {
        'virtualenv_path': None,
    }

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    def run(self, environment=None):
        if environment is None or environment not in self.kwargs['settings']:
            print(red("Please provide a valid environment e.g."))

            for _env in sorted(self.kwargs['settings']):
                print(blue("  fab deploy:{}".format(_env)))
        else:
            self.settings.update(self.kwargs['settings'][environment])
            self.local_settings.update(self.kwargs['local_settings'])

            env.host_string = self.settings['host_string']
            env.user = self.settings['user']

            self.run_task()

    def _run_env(self, cmd):
        if self.settings['use_src']:
            cmd = cmd.replace('manage.py', 'src/manage.py')
        run("source {0}/bin/activate && {1}".format(self.settings['virtualenv_path'], cmd))

    def run_task(self):
        raise NotImplementedError('please implement run_task')

    def _local_env(self, cmd):
        local("source {0}/bin/activate && {1}".format(self.local_settings['virtualenv_path'], cmd))


class Deployment(RemoteTask):
    name = 'deploy'

    def run_task(self):
        print(green("Beginning Deploy:"))

        with cd(self.settings['vhost_path']):
            run("pwd")
            print(green("Pulling master from GitHub..."))
            run("git pull {0}".format(self.settings['branch']))

            if self.settings['install_requirements']:
                self.run_install_requirements()

            if self.settings['less2css']:
                self.run_less2css()

            if self.settings['collect_static']:
                self.run_collect_static()

            if self.settings['syncb_migrate']:
                self.run_syncdb_migrate()

            if self.settings['resetsh']:
                self.run_resetsh()

            if self.settings['compilejsi18n']:
                self.run_compilejsi18n()

            print(green("Restarting Gunicorn"))
            self._run_env("sudo supervisorctl restart {0}".format(self.settings['supervisor_task_name']))

    def run_install_requirements(self):
        print(green("Installing requirements..."))
        self._run_env("pip install -r {0}".format(self.settings['requirements_location']))

    def run_collect_static(self):
        print(green("Collecting static files..."))
        self._run_env("python manage.py collectstatic --noinput")

    def run_syncdb_migrate(self):
        print(green("Syncing the database..."))
        if self.settings['is_django_17_or_higher']:
            self._run_env("python manage.py migrate")
        else:
            self._run_env("python manage.py syncdb --migrate")

    def run_compilejsi18n(self):
        print(green("Collecting static files for jsi18n..."))
        self._run_env("python manage.py compilejsi18n")

    def run_resetsh(self):
        print(green("Executing reset script..."))
        self._run_env("./reset.sh")

    def run_less2css(self):
        print(green("Executing less2css..."))
        self._run_env("lessc {0} > {1}".format(
            self.settings['location_less'],
            self.settings['location_css'],
        ))


class SuperVisorReread(RemoteTask):
    name = 'sv_reread'

    def run_task(self):
        print(green("Rereading supervisor configfiles:"))
        run("sudo supervisorctl reread")


class SuperVisorUpdate(RemoteTask):
    name = 'sv_update'

    def run_task(self):
        print(green("Updating supervisor configfiles:"))
        run("sudo supervisorctl update")


class Clone(RemoteTask):
    name = 'clone'

    def run_task(self):
        print(green("Cloning from environment:"))

        backup_dir = 'ii_temp_backup'
        backup_path = os.path.join(self.settings['vhost_path'], backup_dir)

        backup_zip = 'ii_temp_backup.zip'
        backup_zip_path = os.path.join(self.settings['vhost_path'], backup_zip)

        backup_media = 'media'
        backup_media_path = os.path.join(backup_path, backup_media)

        backup_json = 'fixtures.json'
        backup_json_path = os.path.join(backup_path, backup_json)

        with cd(self.settings['vhost_path']):
            run("pwd")

            print(green("Making backup directory:"))
            run('mkdir {0}'.format(backup_dir))

            print(green("Making fixtures of database:"))
            self._run_env('python manage.py dumpdata --indent=2 --natural --exclude=contenttypes > {0}'.format(backup_json_path))

            print(green("Copying media files:"))
            run('cp -r {0} {1}'.format(self.settings['media_root'], backup_media_path))

            print(green("Making a zip out of it:"))
            run('zip -r {0} {1}'.format(backup_zip_path, backup_dir))

            print(green("Downloading the zip"))
            get(backup_zip_path, backup_zip)

            print(green("Removing the temp-backup files remotely:"))
            run('rm -r {0}'.format(backup_path))
            run('rm {0}'.format(backup_zip_path))

            print(green("Extracting the backup files to a temp directory"))
            local('unzip {0} -d {1}'.format(backup_zip, self.local_settings['path']))

            print(green("Removing the current database:"))
            with cd(self.local_settings['path']):
                self._local_env('python manage.py flush --noinput')

                print(green("Installing the fixtures:"))
                self._local_env('python manage.py loaddata {0}'.format(os.path.join(backup_dir, backup_json)))

                print(green("Copying media files:"))
                local('rm -r {0}'.format(self.local_settings['media_root']))
                local('cp -r {0} {1}'.format(os.path.join(backup_dir, backup_media), self.local_settings['media_root']))

                print(green("Removing the temp-backup files locally:"))
                local('rm -r {0}'.format(backup_dir))
                local('rm {0}'.format(backup_zip))
