Prerequisites
-------------

Before you install and configure the radlogger service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``radloggerpy`` database:

     .. code-block:: none

        CREATE DATABASE radloggerpy;

   * Grant proper access to the ``radloggerpy`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON radloggerpy.* TO 'radloggerpy'@'localhost' \
          IDENTIFIED BY 'RADLOGGERPY_DBPASS';
        GRANT ALL PRIVILEGES ON radloggerpy.* TO 'radloggerpy'@'%' \
          IDENTIFIED BY 'RADLOGGERPY_DBPASS';

     Replace ``RADLOGGERPY_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``radloggerpy`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt radloggerpy

   * Add the ``admin`` role to the ``radloggerpy`` user:

     .. code-block:: console

        $ openstack role add --project service --user radloggerpy admin

   * Create the radloggerpy service entities:

     .. code-block:: console

        $ openstack service create --name radloggerpy --description "radlogger" radlogger

#. Create the radlogger service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        radlogger public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        radlogger internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        radlogger admin http://controller:XXXX/vY/%\(tenant_id\)s
