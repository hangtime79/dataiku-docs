---
title: "Installing deprecated Python versions on DSS 14.0.0"
---

On DSS 14, deprecated Python versions Python 3.6, 3.7 and 3.8 are no longer packaged by default in DCS images. However, they may still be required if your instance relies on these specific versions for compatibility with code environments, plugins, etc.

# Fleet Manager (FM) on version 14.0.0 or later

To install deprecated versions of python on DSS instance that is on version 14.0.0 or later, you may use the "Install deprecated Python" setup action.

How to use:

* Navigate to the instance template in FM
* Click on the "+ Action” button and select the "Install deprecated Python versions (DSS 14 or later)" setup action
* Choose which Python versions you would like to install amongst 3.6, 3.7 and 3.8 (multiple can be toggled at the same time)

> NOTE: Un-toggling a version will not remove the impacted Python versions when replaying the setup actions.
> The instance must be re-provisioned to reset the Python versions installed.

# Fleet Manager (FM) prior to 14.0.0

To address this in FM prior to version 14.0.0, you can use the “Run Ansible tasks” setup action with the appropriate tasks within the instance template of the Dataiku nodes that you would like to upgrade to version 14.0.0.
This action allows you to define and execute custom setup scripts during instance provisioning, making it an ideal place to install Python from source.

You can use the Ansible script defined further to install Python 3.6.15, 3.7.17 and 3.8.20.
However, the script will not install Python versions if an equivalent minor version already exists (e.g. Python 3.6.x or Python 3.7.x).
This action can be replayed and will thus not reinstall the versions of Python that are already present.

How to use:

* Navigate to the instance template in FM.
* Click on the "+ Action” button and select the "Run Ansible tasks" setup action
* As to which stage the script should run during, select "After DSS is started"
* Use the following Ansible script (removing unnecessary Python versions from the script if you do not require them):

```yaml
---
- name: Install required build dependencies
  ansible.builtin.dnf:
    name:
      - "@development"
      - bzip2-devel
      - gdbm-devel
      - libffi-devel
      - libuuid-devel
      - ncurses-devel
      - openssl-devel
      - readline-devel
      - sqlite-devel
      - xz-devel
      - zlib-devel
      - gcc
      - make
      - wget
      - tar
    state: present
    enablerepo: crb

# ---------------- PYTHON 3.6.15 ----------------
- name: Python 3.6 support
  block:
    - name: Check if Python 3.6 is already installed
      command: which python3.6
      environment:
        PATH: "{{ ansible_env.PATH }}:/usr/local/bin"
      register: python36_exists
      changed_when: false
      ignore_errors: true

    - name: Debug message to show Python 3.6 install path
      when: python36_exists.rc == 0
      debug:
        msg: "Python 3.6 is installed at {{ python36_exists.stdout }}"

    - name: Install Python 3.6.15
      when: python36_exists.rc != 0
      block:
        - name: Download Python 3.6.15
          ansible.builtin.get_url:
            url: "https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tgz"
            dest: "/tmp/Python-3.6.15.tgz"
            mode: "755"
            checksum: "md5:f9e6f91c754a604f4fc6f6c7683723fb"

        - name: Extract Python 3.6.15
          ansible.builtin.unarchive:
            src: "/tmp/Python-3.6.15.tgz"
            dest: "/tmp"
            remote_src: true
            mode: "755"

        - name: Write patch file for Python 3.6.15
          ansible.builtin.copy:
            dest: "/tmp/Python-3.6.15/patch36.patch"
            mode: "755"
            content: |
              --- Include/obj.h
              +++ Include/objimpl.h
              @@ -250,7 +250,7 @@
                       union _gc_head *gc_prev;
                       Py_ssize_t gc_refs;
                   } gc;
              -    double dummy;  /* force worst-case alignment */
              +    long double dummy;  /* force worst-case alignment */
               } PyGC_Head;

               extern PyGC_Head *_PyGC_generation0;
              --- Objects/obmalloc.c
              +++ Objects/obmalloc.c
              @@ -643,8 +643,8 @@
                *
                * You shouldn't change this unless you know what you are doing.
                */
              -#define ALIGNMENT               8               /* must be 2^N */
              -#define ALIGNMENT_SHIFT         3
              +#define ALIGNMENT               16               /* must be 2^N */
              +#define ALIGNMENT_SHIFT         4

               /* Return the number of bytes in size class I, as a uint. */
               #define INDEX2SIZE(I) (((uint)(I) + 1) << ALIGNMENT_SHIFT)

        - name: Apply patch for Python 3.6.15
          ansible.posix.patch:
            src: "/tmp/Python-3.6.15/patch36.patch"
            basedir: "/tmp/Python-3.6.15"
            strip: 0

        - name: Configure Python 3.6.15
          ansible.builtin.shell: "./configure > /tmp/Python-3.6.15/configure.txt && rm -f /tmp/Python-3.6.15/configure.txt"
          args:
            chdir: "/tmp/Python-3.6.15"
            creates: "/tmp/Python-3.6.15/Makefile"

        - name: Build Python 3.6.15
          ansible.builtin.shell: "make -j 8 > /tmp/Python-3.6.15/compile.txt && rm -f /tmp/Python-3.6.15/compile.txt"
          args:
            chdir: "/tmp/Python-3.6.15"

        - name: Install Python 3.6.15
          ansible.builtin.shell: "make altinstall > /tmp/Python-3.6.15/install.txt && rm -f /tmp/Python-3.6.15/install.txt"
          args:
            chdir: "/tmp/Python-3.6.15"
            creates: "/usr/local/bin/python3.6"

        - name: Symlink for back compatibility
          become: true
          ansible.builtin.file:
            src: /usr/local/bin/python3.6
            dest: /bin/python3.6
            state: link

        - name: Clean up Python 3.6.15 temporary resources
          ansible.builtin.file:
            path: "{{ item }}"
            state: absent
          loop:
            - /tmp/Python-3.6.15.tgz
            - /tmp/Python-3.6.15

# ---------------- PYTHON 3.7.17 ----------------
- name: Python 3.7 support
  block:
    - name: Check if Python 3.7 is already installed
      command: which python3.7
      environment:
        PATH: "{{ ansible_env.PATH }}:/usr/local/bin"
      register: python37_exists
      changed_when: false
      ignore_errors: true

    - name: Debug message to show Python 3.7 install path
      debug:
        msg: "Python 3.7 is installed at {{ python37_exists.stdout }}"
      when: python37_exists.rc == 0

    - name: Install Python 3.7.17
      when: python37_exists.rc != 0
      block:
        - name: Download Python 3.7.17
          ansible.builtin.get_url:
            url: "https://www.python.org/ftp/python/3.7.17/Python-3.7.17.tgz"
            dest: "/tmp/Python-3.7.17.tgz"
            mode: "755"
            checksum: "md5:19726591b0fb1a9658de68955fa8392a"

        - name: Extract Python 3.7.17
          ansible.builtin.unarchive:
            src: "/tmp/Python-3.7.17.tgz"
            dest: "/tmp"
            remote_src: true
            mode: "755"

        - name: Configure Python 3.7.17
          ansible.builtin.shell: "./configure > /tmp/Python-3.7.17/configure.txt && rm -f /tmp/Python-3.7.17/configure.txt"
          args:
            chdir: "/tmp/Python-3.7.17"
            creates: "/tmp/Python-3.7.17/Makefile"

        - name: Build Python 3.7.17
          ansible.builtin.shell: "make -j 8 > /tmp/Python-3.7.17/compile.txt && rm -f /tmp/Python-3.7.17/compile.txt"
          args:
            chdir: "/tmp/Python-3.7.17"

        - name: Install Python 3.7.17
          ansible.builtin.shell: "make altinstall > /tmp/Python-3.7.17/install.txt && rm -f /tmp/Python-3.7.17/install.txt"
          args:
            chdir: "/tmp/Python-3.7.17"
            creates: "/usr/local/bin/python3.7"

        - name: Symlink for back compatibility
          become: true
          ansible.builtin.file:
            src: /usr/local/bin/python3.7
            dest: /bin/python3.7
            state: link

        - name: Clean up Python 3.7.17 temporary resources
          ansible.builtin.file:
            path: "{{ item }}"
            state: absent
          loop:
            - /tmp/Python-3.7.17.tgz
            - /tmp/Python-3.7.17

# ---------------- PYTHON 3.8.20 ----------------
- name: Python 3.8 support
  block:
    - name: Check if Python 3.8 is already installed
      command: which python3.8
      environment:
        PATH: "{{ ansible_env.PATH }}:/usr/local/bin"
      register: python38_exists
      changed_when: false
      ignore_errors: true

    - name: Debug message to show Python 3.8 install path
      when: python38_exists.rc == 0
      debug:
        msg: "Python 3.8 is installed at {{ python38_exists.stdout }}"

    - name: Install Python 3.8.20
      when: python38_exists.rc != 0
      block:
        - name: Download Python 3.8.20
          ansible.builtin.get_url:
            url: "https://www.python.org/ftp/python/3.8.20/Python-3.8.20.tgz"
            dest: "/tmp/Python-3.8.20.tgz"
            mode: "755"
            checksum: "md5:7e0ff9088be5a3c2fd9b7d8b4b632b5e"

        - name: Extract Python 3.8.20
          ansible.builtin.unarchive:
            src: "/tmp/Python-3.8.20.tgz"
            dest: "/tmp"
            remote_src: true
            mode: "755"

        - name: Configure Python 3.8.20
          ansible.builtin.shell: "./configure > /tmp/Python-3.8.20/configure.txt && rm -f /tmp/Python-3.8.20/configure.txt"
          args:
            chdir: "/tmp/Python-3.8.20"
            creates: "/tmp/Python-3.8.20/Makefile"

        - name: Build Python 3.8.20
          ansible.builtin.shell: "make -j 8 > /tmp/Python-3.8.20/compile.txt && rm -f /tmp/Python-3.8.20/compile.txt"
          args:
            chdir: "/tmp/Python-3.8.20"

        - name: Install Python 3.8.20
          ansible.builtin.shell: "make altinstall > /tmp/Python-3.8.20/install.txt && rm -f /tmp/Python-3.8.20/install.txt"
          args:
            chdir: "/tmp/Python-3.8.20"
            creates: "/usr/local/bin/python3.8"

        - name: Symlink for back compatibility
          become: true
          ansible.builtin.file:
            src: /usr/local/bin/python3.8
            dest: /bin/python3.8
            state: link

        - name: Clean up Python 3.8.20 temporary resources
          ansible.builtin.file:
            path: "{{ item }}"
            state: absent
          loop:
            - /tmp/Python-3.8.20.tgz
            - /tmp/Python-3.8.20
```

* Head to each DSS nodes and in the options, select "Replay Setup Actions" to run the Python Ansible tasks

> NOTE: Once the instance is provisioned, removing a version from the Ansible tasks will not remove the impacted Python versions when replaying the setup actions only.
> The instance must be re-provisioned to reset the Python versions installed.