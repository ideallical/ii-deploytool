import ii_deploytool.tasks as tasks
from fabfile_local import LOCAL_SETTINGS


SETTINGS = {
    'staging': {
        'user': '<user>',
        'host_string': '<host>',
        'vhost_path': '/var/www/pydocs/example-site/s-example-site',
        'use_src': False,  # wheter manage.py is located in project_dir/src or not
        'less2css': False,
        'location_less': '/var/www/pydocs/example-site/s-example-site/project/static/project/css/style.less',
        'location_css': '/var/www/pydocs/example-site/s-example-site/project/static/project/css/style.css',
        'virtualenv_path': '/home/user/virtualenvs/s-example-site',
        'url': 'http://staging.example.com',
        'supervisor_task_name': 'example_site_staging',
        'media_root': '/var/www/pydocs/example-site/s-example-site/media',
    },
    'live': {
        'user': '<user>',
        'host_string': '<host>',
        'vhost_path': '/var/www/pydocs/example-site/l-example-site',
        'use_src': False,  # wheter manage.py is located in project_dir/src or not
        'less2css': False,
        'location_less': '/var/www/pydocs/example-site/l-example-site/project/static/project/css/style.less',
        'location_css': '/var/www/pydocs/example-site/l-example-site/project/static/project/css/style.css',
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
