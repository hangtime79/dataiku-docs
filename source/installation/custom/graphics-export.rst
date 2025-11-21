Setting up DSS item exports to PDF or images
############################################

The Flow, Dashboards and Wiki articles can be exported to PDF or image (PNG, JPG) files in order to share a snapshot of the details within your organization more easily.
The graphics export feature must be setup before DSS items can be exported.


Prerequisites
--------------

* The export feature does not work on Centos 6 and AmazonLinux

* Internet access is required to install additional dependencies required by the export feature

* The account running DSS needs write access to the DSS installation directory at install time;

Precautions
------------

The export feature uses an embedded Chrome browser to perform the actual snapshotting. When you install the feature, an up-to-date Chrome browser is downloaded. We recommend that you regularly perform again the install procedure in order to fetch latest updates, which may be required since Chrome regularly releases security updates.

Security updates of the embedded Chrome browser are not the responsibility of Dataiku.

The embedded Chrome browser is in the ``resources/graphics-export/node_modules`` folder of the DSS installation directory. In case of doubt, you can remove this folder, which will prevent the feature from working.

As of DSS 13.4, this will download and install puppeteer 23.11.1 and its associated headless chromium version (131.0.6778.204) on systems with Node.js is 18+.
For systems with older version of Node.js, this will install the last version of puppeteer that is compatible with the installed Node.js.

Install
--------

* Go to the DSS data dir

* Stop DSS

	.. code-block:: bash

		./bin/dss stop

* Run the installation script

	.. code-block:: bash

		./bin/dssadmin install-graphics-export

* If prompted to, run the dependencies installation script as root

* Start DSS

	.. code-block:: bash

		./bin/dss start

Test the feature by going to a dashboard, in view mode, and clicking Actions > Export.
Alternatively you can test the feature by going to the Flow of a project and clicking Flow Actions > Export to PDF/Image

If you get an error about sandbox mode, it means that the embedded Chrome browser could not start in the most secure "sandbox" mode

Option 1: Enable user namespaces
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The sandbox mode of Chrome runs using a feature of the Linux kernel known as user process namespaces. This feature is not always enabled, you may need to enable it.

Run the following command:

.. code-block:: bash

	sysctl user.max_user_namespaces

If the result is 0, run the following command as root:

.. code-block:: bash

	sysctl user.max_user_namespaces=1000

If the result was 0 in the previous step, you will also want to add this entry to your ``/etc/sysctl.conf`` file so that this setting is retained upon server reboot:

.. code-block:: bash 

    # edit your /etc/sysctl.conf file 
    sudo vi /etc/sysctl.conf
    
    # add the following entry to the end of the file 
    user.max_user_namespaces=1000    

Then retry exporting the Flow or dashboard

Option 2: Disable sandbox
%%%%%%%%%%%%%%%%%%%%%%%%%%%

If you are not able to run the previous, or if it fails (which may be possible if you have a too old kernel), you can disable the additional sandbox protection. The sandbox is a "second level" of security to mitigate exploitation possibilities in case of a security bug in Chrome.

* Edit the ``config/dip.properties`` file

* Add the following line: ``dku.exports.chrome.sandbox=false``

* Restart DSS
