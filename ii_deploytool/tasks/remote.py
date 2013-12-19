from fabric.api import cd, env, run
from fabric.colors import blue, green, red
from fabric.tasks import Task


class RemoteTask(Task):
    settings = {
        'install_requirements': True,
        'collect_static': True,
        'syncb_migrate': True,
        'resetsh': False,
        'compilejsi18n': False,
    }

    def __init__(self, *args, **kwargs):
        self.kwargs=kwargs

    def run(self, environment=None):
        if environment is None or environment not in self.kwargs['settings']:
            print(red("Please provide a valid environment e.g."))

            for _env in sorted(self.kwargs['settings']):
                print(blue("  fab deploy:{}".format(_env)))
        else:
            self.settings.update(self.kwargs['settings'][environment])

            env.host_string = self.settings['host_string']
            env.user = self.settings['user']

            self.run_task()

    def _run_env(self, cmd):
        run("source {0}/bin/activate && {1}".format(self.settings['virtualenv_path'], cmd))

    def run_task(self):
        raise NotImplementedError('please implement run_task')


class Deployment(RemoteTask):
    name = 'deploy'

    def run_task(self):
        print(green("Beginning Deploy:"))

        with cd(self.settings['vhost_path']):
            run("pwd")
            print(green("Pulling master from GitHub..."))
            run("git pull origin master")

            if self.settings['install_requirements']:
                self.run_install_requirements()

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
        self._run_env("pip install -r requirements.txt")

    def run_collect_static(self):
        print(green("Collecting static files..."))
        self._run_env("python manage.py collectstatic --noinput")

    def run_syncdb_migrate(self):
        print(green("Syncing the database..."))
        self._run_env("python manage.py syncdb --migrate")

    def run_compilejsi18n(self):
        print(green("Collecting static files for jsi18n..."))
        self._run_env("python manage.py compilejsi18n")

    def run_resetsh(self):
        print(green("Executing reset script..."))
        self._run_env("./reset.sh")


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
