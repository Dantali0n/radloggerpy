================================
Command line interface reference
================================

.. autoprogram-cliff:: radloggerpy.radloggercli.RadLoggerShell
   :application: radloggercli

.. raw:: html

    <div class="section" id="complete">
        <h2>complete<a class="headerlink" href="#complete" title="Permalink to this headline">¶</a></h2>

The ``complete`` command is inherited from the `python-cliff` library, it can
be used to generate a bash-completion script. Currently, the command will
generate a script for bash versions 3 or 4. The bash-completion script is
printed directly to standard out.

Typical usage for this command is:

.. code-block:: bash

  radloggercli complete | sudo tee /etc/bash_completion.d/radloggercli > /dev/null

.. raw:: html

    </div>

.. autoprogram-cliff:: radloggerpy.cli.v1
   :application: radloggercli
