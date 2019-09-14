2. Edit the ``/etc/radloggerpy/radloggerpy.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://radloggerpy:RADLOGGERPY_DBPASS@controller/radloggerpy
