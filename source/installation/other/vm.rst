Install a virtual machine
#############################

Dataiku provides a pre-built virtual machine for Virtualbox and VMWare player.
This allows you to install DSS if you only have access to a Windows machine.

.. contents::
	:local:

Installation instructions and details are available here: https://www.dataiku.com/dss/trynow/virtualbox/ - please read carefully the following prerequisites.

Prerequisites
================

CPU and OS
------------

You need to have a 64 bits CPU, with a 64 bits OS. The virtual machine will not start without.

On Windows, you can check that you have a 64 bits CPU and a 64 bits OS by going to the System information window.

.. image:: img/64-bits-cpu.png

.. _install-other-vm-hw:

Hardware virtualization
--------------------------


Hardware virtualization is mandatory for the DSS virtual machine. This is generally called "AMD-V" or "VT-x".

All 64 bits CPU support hardware virtualization, but it is often disabled in the BIOS/UEFI of the machines.

If hardware virtualization is missing, the virtual machine will not start and emit messages like ``VT-x is not available (VERR_VMX_NO_VMX).`` or ``VT-x is disabled in the BIOS for all CPU modes (VERR_VMX_MSR_ALL_VMX_DISABLED).``

The following links provide some help on how to enable hardware virtualization:

* https://www.google.com/search?q=VT-x+is+not+available+(VERR_VMX_NO_VMX).
* https://www.howtogeek.com/213795/how-to-enable-intel-vt-x-in-your-computers-bios-or-uefi-firmware/
* http://druss.co/2015/06/fix-vt-x-is-not-available-verr_vmx_no_vmx-in-virtualbox/


.. _install-other-vm-mem:

Host memory
------------

It is strongly recommended that you have at least 8 GB of RAM to run the DSS virtual machine.

The DSS virtual machine is preconfigured to use 4 GB of memory. If you only have 4 or 6 GB of memory, your host might become unresponsive when starting the DSS virtual machine. If you have less than 8 GB of RAM, we strongly recommend that you lower the amount of memory allocated to the DSS virtual machine before starting it. You can go as low as 2 GB of memory for the DSS virtual machine.

Hypervisor
------------

The DSS virtual machine is provided as a .ova file that can be opened with Virtualbox or VMWare.

If you use VMWare Player, you'll encounter a warning while importing the OVA file. You can ignore it and select "Retry".

Installation
=============

Step by step instructions are available at https://www.dataiku.com/dss/trynow/virtualbox/

How do I use DSS?
-------------------

When the virtual machine starts up, it starts by displaying a "DSS is starting" message. When startup is complete, the virtual machine displays a connection banner like this one:

.. image:: img/startup-ok.png

You need to open your browser on the URL referenced as "Data Science Studio interface"

Troubleshooting
=================

VT-x is not available (VERR_VMX_NO_VMX)
-----------------------------------------

This error means that hardware virtualization is not enabled.

See :ref:`install-other-vm-hw`

VT-x is disabled in the BIOS for all CPU modes (VERR_VMX_MSR_ALL_VMX_DISABLED)
----------------------------------------------------------------------------------

This error means that hardware virtualization is not enabled.

See :ref:`install-other-vm-hw`

The URL to connect does not appear
-----------------------------------

When the virtual machine starts up, it starts by displaying a "DSS is starting" message.

.. image:: img/vm-starting.png

When startup is complete, the virtual machine displays a connection banner like this one:

.. image:: img/startup-ok.png

If, after 5-10 minutes, this connection banner is still not displayed and you instead still have the "DSS starting" message, the most probable cause is that your machine does not have enough memory to run both your regular OS and the DSS virtual machine, and the host machine is swapping. We strongly recommend having 8 GB of RAM to run the DSS virtual machine. You can also try to lower the memory allocated to the virtual machine to around 2 GB.

Please see: :ref:`install-other-vm-mem`

The URL to connect does not work
---------------------------------

When you connect to the "Data Science Studio interface" URL, the Dataiku registration page should appear.

If it does not appear and you get a browser error message like:

* Connection timeout
* Connection refused

The most probable cause is that you have a corporate security suite (like McAfee Total Security) that restricts connection from your host machine to the virtual machine. If this is the case:

* You might be able to ask your security administrator for more details
* In some cases, VMWare player is an approved application, and switching from Virtualbox to VMWare player might work.

However, fairly often, this kind of problem is not workaroundable (meaning you won't be able to use the DSS virtual machine) as it is part of the company corporate security policy. See below for other options.


How to
=======

I cannot get the virtual machine to work
------------------------------------------

If you cannot meet the prerequisites or are blocked by a corporate security system, you might want to try our cloud installation options: :doc:`aws`  or :doc:`azure`.

You might also want to try a hosted trial of DSS (running on Dataiku's servers): https://www.dataiku.com/dss/trynow

How do I log into the virtual machine?
----------------------------------------

Note that you do not need to log into the virtual machine to simply run DSS. See above documentation.

If you need to log into the virtual machine console (for troubleshooting or installing additional software), use the console login prompt. Login details (login and password) are displayed in the welcome banner of the virtual machine.

Where is the DSS data directory?
----------------------------------

DSS is installed in ``/home/dataiku/dss``

How do I check if DSS is running?
-----------------------------------

* Login to the instance as detailed above
* Go to the DSS data directory : ``cd /home/dataiku/dss``
* Run ``./bin/dss status``
* The status should display all processes as ``RUNNING``.

How do I install JDBC drivers?
-------------------------------

JDBC drivers must be installed by copying the relevant files in the "lib/jdbc" folder of the DSS data directory (See :doc:`/installation/custom/jdbc`).

To upload files to the DSS data directory, the best solution is to use WinSCP to connect to the virtual machine. The SSH connection details are displayed in the welcome banner of the virtual machine. The DSS data directory is ``/home/dataiku/dss``