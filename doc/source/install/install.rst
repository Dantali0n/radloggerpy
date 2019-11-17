.. _install:

.. role:: bash(code)
   :language: bash

Install and configure
~~~~~~~~~~~~~~~~~~~~~

This section describes how to install and configure the RadLogger service,
code-named RadLoggerPy. However, this installation and configuration procedure
varies per Linux distribution. The recommended method of installation is
through *virtualenv* which will resolve most distribution specific procedures.
However, the installation method for Python, Pip and virtualenv are still
different depending on the package manager used by the distribution.
Installation through virtualenv will ensure that Python packages and
executables are only available when the virtualenv is activated. This prevents
potential pip conflicts but requires that the environment is activated before
RadLoggerPy can be run. Additionally, the system wide installation offers
Systemd service files while virtualenv will not install these.

**Install dependencies:**
 Arch:
    :bash:`pacman -Syu python python-virtualenv python-pip`
 Debian & Ubuntu:
    :bash:`sudo apt update && sudo apt install python3 python3-virtualenv
    python3-pip`
 CentOS 8:
    :bash:`sudo yum -y install python3 python3-pip python3-virtualenv`
 CentOS 7.5:
    .. code-block:: bash

        sudo yum update
        sudo yum install yum-utils
        sudo yum groupinstall development
        sudo yum install https://centos7.iuscommunity.org/ius-release.rpm
        sudo yum install python36u
        sudo yum install python36u-pip
        sudo yum install python36u-devel

Installing RadLogger with virtualenv
####################################

Start by downloading the `latest release`_ from Github and unpacking it into a
desired directory. Alternatively the release can also be downloaded using git
with. Next, a virtualenv can be created in any desired directory, however, this
environment should be located in a convenient location.

.. code-block:: bash

    git clone https://github.com/Dantali0n/radloggerpy.git`
    cd radloggerpy
    tox -e venv
    source .tox/venv/bin/active
    python setup.py install

.. _`latest release`: https://github.com/Dantali0n/radloggerpy/archive/master.zip
