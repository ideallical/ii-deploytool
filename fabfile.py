import ii_deploytool.tasks as tasks


SETTINGS = {
    'staging': {
        'user': '<user>',
        'host_string': '<host>',
        'vhost_path': '/var/www/pydocs/example-site/s-example-site',
        'virtualenv_path': '/home/user/virtualenvs/s-example-site',
        'url': 'http://staging.example.com',
        'supervisor_task_name': 'example_site_staging',
    },
    'live': {
        'user': '<user>',
        'host_string': '<host>',
        'vhost_path': '/var/www/pydocs/example-site/l-example-site',
        'virtualenv_path': '/home/user/virtualenvs/example-site',
        'url': 'http://example.com',
        'supervisor_task_name': 'example_site_live',
    }
}

# deployment
deploy = tasks.remote.Deployment(settings=SETTINGS)

# supervisor
sv_reread = tasks.remote.SuperVisorReread(settings=SETTINGS)
sv_update = tasks.remote.SuperVisorUpdate(settings=SETTINGS)
