import ii_deploytool.tasks as tasks
from fabfile_local import LOCAL_SETTINGS


SETTINGS = {
    'staging': {
        'user': '<user>',
        'host_string': '<host>',
        'vhost_path': '/var/www/pydocs/example-site/s-example-site',
        'virtualenv_path': '/home/user/virtualenvs/s-example-site',
        'url': 'http://staging.example.com',
        'supervisor_task_name': 'example_site_staging',
        'media_root': '/var/www/pydocs/example-site/s-example-site/media',
    },
    'live': {
        'user': '<user>',
        'host_string': '<host>',
        'vhost_path': '/var/www/pydocs/example-site/l-example-site',
        'virtualenv_path': '/home/user/virtualenvs/example-site',
        'url': 'http://example.com',
        'supervisor_task_name': 'example_site_live',
        'media_root': '/var/www/pydocs/example-site/l-example-site/media',
    }
}

# deployment
deploy = tasks.remote.Deployment(settings=SETTINGS, local_settings=LOCAL_SETTINGS)

# supervisor
sv_reread = tasks.remote.SuperVisorReread(settings=SETTINGS, local_settings=LOCAL_SETTINGS)
sv_update = tasks.remote.SuperVisorUpdate(settings=SETTINGS, local_settings=LOCAL_SETTINGS)

# handy
clone = tasks.remote.Clone(settings=SETTINGS, local_settings=LOCAL_SETTINGS)
