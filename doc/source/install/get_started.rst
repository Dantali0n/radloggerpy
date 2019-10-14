==========================
radlogger service overview
==========================
The radlogger service provides an interactive or background daemon that will
monitor background radiation. This is achieved by interfacing with a variety
of radiation logger or 'geiger counter' devices. Subsequently, the retrieved
information is stored in a local database and can be submitted to one or more
online radiation monitoring services if desired.

The radlogger service consists of the following components:

``radloggerpy`` service
  Runs as a daemon connecting to the geiger counter and logging
  data to a sqlite database.
