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

**This guide does not reflect the currently implemented features but rather
the intended features and operation!**

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

This theory of operation concerns the ``radloggerpy`` service beginning when the
service is launched.

Early initialization:
*********************

Initially, the service loads configuration and sets up logging, afterwards
the logo is displayed depending on the settings. When this basic initialization
is finalized all devices are initialized as shown in the flow-chart below. Here
the :boldorange:`orange` line indicates the launch of a new thread, however,
the number of threads spawned is user configurable. The underlying threadpool
will decide when devices are scheduled to run. After the basic initialization of
a device it enters an active loop from which it still can enter an error state
if problems are encountered. The active loop itself is not shown here.

Upon encountering a device error several methods will be available to notify
users. These can be enabled in the configuration along with any configuration
parameters required. Upon encountering errors devices can be scheduled for
restart depending on user configuration. However, this is not considered a part
of early initialization.

..
    fg-device-init.xml

.. image:: /images/fg-device-init.svg
    :align: center
    :width: 100%
    :alt: Device initialization flow chart



Device States:
**************

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

Device to Endpoint Communication:
*********************************

When :boldgreen:`devices` are running they generate messages, to store or
transmit these each message must be passed to a so called
:boldyellow:`endpoint`. :boldgreen:`Devices` communicate with
:boldyellow:`endpoints` using the publish subscribe pattern. There are two
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
