================
Developers guide
================

.. role:: boldorange
  :class: orange bolditalic

This section covers several topics about RadLoggerPy that are likely to
eventually make it into the general documentation but in a more refined
condensed form. This documentation serves as indication for other developers
but decisions can always be refined and changed later.

Diagrams:
#########

Diagrams should be made using draw.io and submitted as xml export in the
diagrams folder with the commit that introduces the diagram. The image export
should be placed in the images folder and svg is the preferred format. There
is no absolute standard upheld to create diagrams but describing distinct
visual attributes and or including a legend is required. When a image of a
diagram is used a comment above it should reference the source xml file. Having
identical names is preferred.

Theory of operation:
####################

This operation concerns the ``radloggerpy`` service beginning when the service
is launched. The service loads configuration and sets up logging, afterwards
the logo is displayed depending on the settings. When this basic initialization
is finalized all devices are initialized as shown in the flow-chart below. Here
the :boldorange:`orange` line indicates the launch of a new thread. After the
basic initialization of a device it enters an active loop from which it still
can enter an error state if problems are encountered. The active loop itself is
not shown here.

..
    fg-device-init.xml

.. image:: /images/fg-device-init.svg
    :align: center
    :width: 100%
    :alt: Device initialization flow chart

Upon encountering a device error several methods will be available to notify
users. These can be enabled in the configuration along with any configuration
parameters required.
