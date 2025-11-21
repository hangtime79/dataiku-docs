---
title: "Adding deprecated Python versions support to DSS 14 Docker images for containerized execution and API nodes"
---

DSS 14 base images (containerized execution, CDE, API node image) does not contain deprecated Python versions 3.6, 3.7 and 3.8 by default anymore.
In order to create images for code environments using these interpreters, they must be installed prior to creating the code environment in the image.

For code environments used solely for the purpose of API services that will be deployed to API nodes, only the first code environment in the API service endpoints requires the container runtime addition or the Dockerfile additions outlined below.

# Using container runtime additions

For most installations, in the code environment menu, in "Containerized execution", there is a section called "Container runtime additions".
This is used to install dependencies for the code environment image without including them in the base image.

Click "ADD" and choose in the list the Python installation item that corresponds to your code environment (Python 3.6, Python 3.7 or Python 3.8).

You can then save and update the code environment to create the image with the required Python interpreter installed.

# Using advanced container settings

For installations where the container runtime addition may not work, the Python versions may still be added to the code environment image.
In the code environment menu, in "Containerized execution", you will find the "Advanced container settings" section.
The following Dockerfile statements may be added in the "At-start Dockerfile" section for each version of the deprecated Python versions:

- Python 3.6:
```Dockerfile
# Install development tools and dependencies needed to compile Python 3.6
RUN dnf groupinstall -y "Development Tools" && \
    dnf install -y \
    openssl-devel \
    libffi-devel \
    bzip2-devel \
    readline-devel \
    sqlite-devel \
    wget \
    curl \
    ncurses-devel \
    xz-devel \
    tk-devel \
    libxml2-devel \
    libxslt-devel \
    zlib-devel \
    && dnf clean all

# Download and compile Python 3.6.15 (latest 3.6 release) with alignment patch
RUN cd /tmp && \
    curl -OsS https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tgz && \
    tar xzf Python-3.6.15.tgz

WORKDIR /tmp/Python-3.6.15

# Create and apply alignment patch
RUN echo '--- Include/objimpl.h.orig' >> alignment.patch && \
    echo '+++ Include/objimpl.h' >> alignment.patch && \
    echo '@@ -250,7 +250,7 @@' >> alignment.patch && \
    echo '         union _gc_head *gc_prev;' >> alignment.patch && \
    echo '         Py_ssize_t gc_refs;' >> alignment.patch && \
    echo '     } gc;' >> alignment.patch && \
    echo '-    double dummy;  /* force worst-case alignment */' >> alignment.patch && \
    echo '+    long double dummy;  /* force worst-case alignment */' >> alignment.patch && \
    echo ' } PyGC_Head;' >> alignment.patch && \
    echo ' ' >> alignment.patch && \
    echo ' extern PyGC_Head *_PyGC_generation0;' >> alignment.patch && \
    echo '--- Objects/obmalloc.c.orig' >> alignment.patch && \
    echo '+++ Objects/obmalloc.c' >> alignment.patch && \
    echo '@@ -643,8 +643,8 @@' >> alignment.patch && \
    echo '  *' >> alignment.patch && \
    echo "  * You shouldn't change this unless you know what you are doing." >> alignment.patch && \
    echo '  */' >> alignment.patch && \
    echo '-#define ALIGNMENT               8               /* must be 2^N */' >> alignment.patch && \
    echo '-#define ALIGNMENT_SHIFT         3' >> alignment.patch && \
    echo '+#define ALIGNMENT               16              /* must be 2^N */' >> alignment.patch && \
    echo '+#define ALIGNMENT_SHIFT         4' >> alignment.patch && \
    echo ' ' >> alignment.patch && \
    echo ' /* Return the number of bytes in size class I, as a uint.' >> alignment.patch && \
    echo ' #define INDEX2SIZE(I) (((uint)(I) + 1) << ALIGNMENT_SHIFT)' >> alignment.patch && \
    patch -N -p0 < alignment.patch

RUN cat alignment.patch

# Configure, compile, and install Python 3.6 with optimizations
RUN ./configure --enable-optimizations --with-ensurepip=install > configure.txt && \
    make -j 8 altinstall > install.txt && \
    rm -rf /tmp/Python-3.6.15*

# Upgrade pip and setuptools to latest versions
RUN /usr/local/bin/python3.6 -m pip install --upgrade pip setuptools

# Clean up installation to reduce image size
RUN cd /usr/local/lib/python3.6/test && \
    ls | grep -vx support | xargs rm -rf && \
    cd /usr/local/lib && \
    rm -f libpython3.6*.a && \
    rm -f python3.6/config-3.6*-*/libpython3.6*.a && \
    find python3.6 -depth -type f -name '*.pyc' -exec rm -f {} \;

WORKDIR /opt/dataiku
```

- Python 3.7:
```Dockerfile
# Install development tools and dependencies needed to compile Python 3.7
RUN dnf --setopt=group_package_types=mandatory --enablerepo=crb groupinstall -y "Development Tools" && \
    dnf install -y \
        bzip2-devel \
        gdbm-devel \
        libffi-devel \
        libuuid-devel \
        ncurses-devel \
        openssl-devel \
        readline-devel \
        sqlite-devel \
        xz-devel \
        zlib-devel && \
    dnf clean all

# Download and compile Python 3.7.17 (latest 3.7 release)
RUN cd /tmp && \
    curl -OsS https://www.python.org/ftp/python/3.7.17/Python-3.7.17.tgz && \
    tar xzf Python-3.7.17.tgz && \
    cd Python-3.7.17 && \
    ./configure --enable-optimizations --with-ensurepip=install  > configure.txt && \
    make -j 8 altinstall > install.txt && \
    rm -rf /tmp/Python-3.7.17*

# Upgrade pip and setuptools to latest versions
RUN /usr/local/bin/python3.7 -m pip install --upgrade pip setuptools

# Clean up installation to reduce image size
RUN cd /usr/local/lib/python3.7/test && \
    ls | grep -vx support | xargs rm -rf && \
    cd /usr/local/lib && \
    rm -f libpython3.7*.a && \
    rm -f python3.7/config-3.7*-*/libpython3.7*.a && \
    find python3.7 -depth -type f -name '*.pyc' -exec rm -f {} \;
```

- Python 3.8:
```Dockerfile
# Install development tools and dependencies needed to compile Python 3.8
RUN dnf --setopt=group_package_types=mandatory --enablerepo=crb groupinstall -y "Development Tools" && \
    dnf install -y \
        bzip2-devel \
        gdbm-devel \
        libffi-devel \
        libuuid-devel \
        ncurses-devel \
        openssl-devel \
        readline-devel \
        sqlite-devel \
        xz-devel \
        zlib-devel && \
    dnf clean all

# Download and compile Python 3.8.20 (latest 3.8 release)
RUN cd /tmp && \
    curl -OsS https://www.python.org/ftp/python/3.8.20/Python-3.8.20.tgz && \
    tar xzf Python-3.8.20.tgz && \
    cd Python-3.8.20 && \
    ./configure --enable-optimizations --with-ensurepip=install > configure.txt && \
    make -j 8 altinstall > install.txt && \
    rm -rf /tmp/Python-3.8.20*

# Upgrade pip and setuptools to latest versions
RUN /usr/local/bin/python3.8 -m pip install --upgrade pip setuptools

# Clean up installation to reduce image size
RUN cd /usr/local/lib/python3.8/test && \
    ls | grep -vx support | xargs rm -rf && \
    cd /usr/local/lib && \
    rm -f libpython3.8*.a && \
    rm -f python3.8/config-3.8*-*/libpython3.8*.a && \
    find python3.8 -depth -type f -name '*.pyc' -exec rm -f {} \;
```

You may change the Python download URLs as you see fit for airgapped instances or partial internet access.