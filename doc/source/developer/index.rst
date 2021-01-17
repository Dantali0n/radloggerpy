================
Developers guide
================

.. role:: boldorange
  :class: orange bolditalic

.. role:: boldgreen
  :class: green bolditalic

.. role:: boldyellow
  :class: yellow bolditalic

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
the :boldorange:`orange` line indicates the launch of a new thread, however,
the number of threads spawned is user configurable. The underlying threadpool
will decide when devices are scheduled unto the configured threads if the
number of devices exceeds the configured maximum number of threads. After the
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

The state transition diagram below shows the different states devices can be in
and how they can transition between states. Implementations of devices do not
have to manage these transitions themselves, instead the abstract device run
method will handle these transitions. Devices only need to ensure they raise
the appropriate errors upon encountering them.

..
    st-device-states.xml

.. image:: /images/st-device-states.svg
    :align: center
    :width: 100%
    :alt: Device state transition diagram

When :boldgreen:`devices` are running they generate messages, to store or
transmit these each message must be passed to a so called
:boldyellow:`endpoint`. :boldgreen:`Devices` communicate with
:boldyellow:`endpoints` to through the publish subscribe pattern. There are two
fundamental types of messages. Those from continuous readings and those from
average readings. Notably, a :boldgreen:`device` measuring continuously can
also generate average readings but does not have to support this. If a single
:boldyellow:`endpoint` supports both continuous and average readings it must be
developed as two separate :boldyellow:`endpoint` classes.

..
    comm-device-endpoint.xml

.. image:: /images/comm-device-endpoint.svg
    :align: center
    :width: 100%
    :alt: Device to endpoint communication
