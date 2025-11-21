# Howto: Operate DSS behind a proxy/firewall that filters URL

  * [1. Overview](#1-overview)
  * [2. System packages](#2-system-packages)
  * [3. Python](#3-python)
  * [4. R](#4-r)
  * [5. Plugins](#5-plugins)


<a name="1-overview"></a>

## 1. Overview

This document provides a set of recommended whitelists when DSS is operated on a corporate network that is protected by a proxy/firewall that filters allowed URLs.

While DSS is designed to be able to operate in a fully isolated environment without any kind of Internet access, this significantly restricts the ability to work with Python and R packages.


<a name="2-system-packages"></a>

## 2. System packages

DSS requires that you have the ability to install system packages, either directly from the upstream distribution, or from a local mirror.

This includes additional repositories that are non standard.

The precise list of packages and repositories is documented in the DSS reference documentation:
https://doc.dataiku.com/dss/latest/installation/new_instance.html#manual-dependency-installation

<a name="3-python"></a>

# 3. Python packages

The DSS installation directory comes with all Python packages that are required to operate DSS. If you don't plan to add additional Python packages, you don't need anything more.

However, without additional Internet access:

* You won't be able to create your own Python code environments
* You won't be able to add any Python package

## 3.1 Using pip

Please note that the Python packaging ecosystem:

* Is designed in such a way that there is not a single repository containing all packages
* Is fast-evolving

The download location is not necessarily on PyPI. The Python package index is a metadata service, one that happens to also provide storage for the indexed packages. As such, not all packages indexed on PyPI are actually downloaded from PyPI, the download location could be anywhere on the internet.

However, this initial list should give you most packages:

* https://pypi.python.org/
* https://pythonhosted.org/
* https://pypi.org

If individual package installations fail, check their PyPI page and add the download location listed for those.

## 3.2 Using conda

Whitelist the following:

* https://conda.binstar.org/numba/win-64/
* https://conda.anaconda.org/
* https://binstar.org/
* https://anaconda.org/
* https://repo.continuum.io/
* https://pypi.python.org/

We recommend that you also whitelist the Pypi URLs.

<a name="4-r"></a>

# 4. R packages

The DSS installation kit does not come with R packages builtin.

In order to install R packages and R code envs, you need to whitelist the following:

* https://cran.rstudio.com
* https://cloud.r-project.org

Or any of the other cran mirrors: https://cran.r-project.org/mirrors.html

Alternatively, you can use our offline installation procedure, but this will only allow you to install base R packages, not further code environments


<a name="5-plugins"></a>

# 5. Dataiku Plugins and Tutorials

Whitelist: 

* https://www.dataiku.com/product/plugins/

To install plugins that are not on the official store or if your server doesn’t have Internet access, you need first to obtain the Zip file of the plugin.

For official plugins, obtain the Zip archive from: https://www.dataiku.com/community/plugins

# 6. NGINX

In some instances the url for nginx needs to be whitelisted. Please check with the internal IT to see if this is allowed. If not add it to the whitelist.
https://nginx.org/

# 7. Recommended content banner and help center
To use the Dataiku homepage's recommended content banner and access the help center, ensure that your browser can connect to the following hosts:

* https://help.dataiku.com/ 
* https://doc.dataiku.com/
* https://knowledge.dataiku.com/
* https://developer.dataiku.com/
* https://academy.dataiku.com/
* https://blog.dataiku.com/
* https://community.dataiku.com/
* https://www.dataiku.com/