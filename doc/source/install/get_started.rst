==========================
RadLogger service overview
==========================
The RadLogger service provides an a background daemon that will monitor
background radiation. This is achieved by interfacing with a variety of
radiation logger or 'geiger counter' devices. Subsequently, the retrieved
information is stored in a local database and can be submitted to one or more
online radiation monitoring services if desired.

To configure which devices exist as well as other settings an interactive
command line interface is available. This interface can either take a series of
arguments to perform a command and return the shell or be ran interactively
until terminated by user command.

The RadLogger service consists of the following components:

``radloggerpy`` service
  Runs as a daemon connecting to the geiger counters, logging data to a
  sqlite database and uploading it to relevant platforms.

``radloggercli`` service
  Takes user command line arguments to perform tasks such as adding devices
  or platforms.
