===========================
ideallical - deploytool 0.1
===========================

Project application for deployment, provisioning and local tasks.


Remote requirements
===================

* Debian / Ubuntu
* Nginx
* MySQL
* MySQL-python
* MySQL-devel
* OpenSSH
* Pip (1.1+)
* Python (2.7)
* python-devel
* sudo
* virtualenv (1.6+)
* zip


Local requirements
==================

* Fabric (1.8+)
* Git (1.6+)
* unzip


Usage
=====

Install ii-deploytool

::

    $ pip install ii-deploytool


Add a fabfile.py in the root folder of your Django project. An example can be found here:

::
    https://github.com/ideallical/ii-deploytool/fabfile.py

Add a fabfile_local.py in the root folder of your Django project. An example can be found here:

::
    https://github.com/ideallical/ii-deploytool/fabfile_local.py


Deploy with:

::
    $ fab deploy:dev


Clone remote environment with:

::
    $ fab clone:live
