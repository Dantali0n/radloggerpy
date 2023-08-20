===================
Configuration Guide
===================

The static configuration for RadLoggerPy lives should be placed in:
``radloggerpy.conf`` and it is described below.

Configuration
-------------

RadLoggerPy, like most OpenStack projects, uses INI-style configuration files to
configure various services and utilities. This functionality is provided by the
`oslo.config`__ project. *oslo.config* supports loading configuration from both
individual configuration files and a directory of configuration files. By
default, RadLoggerPy will search the below directories for the config files -
``radloggerpy.conf`` and ``{prog}.conf``, where ``prog`` corresponds to the name
of the service or utility being configured such as :program:`raddloggercli`:

- ``${HOME}/.radloggerpy``
- ``${HOME}``
- ``/etc/radloggerpy``
- ``/etc``

Where a matching file is found, all other directories will be skipped.
This behavior can be overridden by using the ``--config-file`` and
``--config-dir`` options provided for each executable.

.. __: https://docs.openstack.org/oslo.config/latest/

Configuration Parameters
------------------------

.. show-options::

   radloggerpy

Sample Configuration
--------------------

.. important::

   The sample configuration file is auto-generated from RadLoggerPy when this
   documentation is built. You must ensure your version of RadLoggerPy matches
   the version of this documentation.

.. literalinclude:: /_static/radloggerpy.conf.sample
