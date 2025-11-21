# dss-doc


Run this using a **python == 3.8** (due to `snowflake-snowpark-python` Python version requirement)

Note: if you use a MacOS with ARM architecture, you use the intel environement to have Python 3.8 (including installing pyenv and virtualenv in intel env)

* At the top level: a Sphinx project with the ref doc (https://doc.dataiku.com)
* In developer-guide: a Sphinx project with the developers' guide (https://developer.dataiku.com)
* In app-notes: the app notes


## How to build the ref doc and developer guide

* Have a clone of the dip repository
* Create a Python env with Python 3.8
* Open an intel terminal
```
pyenv virtualenv 3.8.20 myenv38-dssdoc
```
* Activate it
```
pyenv activate myenv38-dssdoc
```

* Make sure the configuration is used after restarting
```
pyenv local myenv38-dssdoc
```
* Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
export DKUINSTALLDIR=/path/to/a/dip/clone/ # already set if using direnv
export PYTHONPATH=$DKUINSTALLDIR/src/main/python:$DKUINSTALLDIR/lambda/src/main/python/dataiku/apinode:/path/to/a/spark/clone/python:./python
```
Replace the `/path/to/a/dip/clone` with the correct path to **YOUR** dip-cloned repository.

To build the refdoc:
```
make html
```

To build the DevGuide:
```
cd developer-guide && make html
```

The doc is in `build/html` and `developer-guide/build/html`.
You can directly browse the generated documentation by accessing `build/html/index.html`
and `developer-guide/build/html/index.html` in your browser.

## macOS ARM Config for Visual Studio Code
When working on a macOS ARM machine, you can automate running the `intel` command when the Visual Studio Code terminal opens. Create a `.vscode/settings.json` file in your project, and add the following content. Make sure the `path` is correct for your environment.

```json
{
    "terminal.integrated.profiles.osx": {
        "intel setup": {
            "path": "/usr/bin/arch",
            "args": [
                "-x86_64",
                "/bin/zsh",
                "--login"
            ]
        }
    },
    "terminal.integrated.defaultProfile.osx": "intel setup"
}
```

## Interactive server (developer-guide only)

* Launch a local web server, which will make the Developer Guide available at [http://localhost:8000](http://localhost:8000):

  ```bash
  # From the developer-guide/ directory
  make serve
  ```

If you modify the refdoc to add a new anchor (for example) and want to refer to it in the devguide,
you won't see the result. This is due to intersphinx mapping (in the devguide),
which refers to `http://doc.dataiku.com`. So, a local modification is not pushed to the live documentation.

Nevertheless, you can see the result locally by following these steps:

* Modify the refdoc (according to your needs)
* Serve the refdoc locally
  * To be able to serve the doc locally, you need to create a live server:
     * Create an environment variable `DSS_DOC_DIR` that points to the refdoc directory
     *  A live server could be created by using (and running) the following code:
        ```python
        import http.server
        import socketserver
        import os

        PORT = 7000
        DIRECTORY = f"{os.getenv('DSS_DOC_DIR')}/build/html/"


        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=DIRECTORY, **kwargs)


        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()
        ```
    * This code will serve the refdoc to http://localhost:7000/ .If you need, you can change the PORT number to avoid conflict with an already used port. If you do so, you have to accordingly update the URL.
* Modify the intersphinx mapping in the devGuide
  * Edit the file `developer-guide/source/conf.py` by changing the line:
    ```
    intersphinx_mapping = {'refdoc': ('https://doc.dataiku.com/dss/latest/', None)}
    ```
    to
    ```
    intersphinx_mapping = {'refdoc': ('http://localhost:7000', None)}
    ```
* Make the devguide
* Be sure to avoid committing the `conf.py` modification.


## Expected warnings

Some warnings are expected and normal:

* `WARNING: document isn't included in any toctree`:
    * normal for pages starting with `_` (included in other pages via `include` directive)
    * expected for `source/thirdparty-build.rst`, which we want to  publish but not link/list


## Contributing to the refdoc

The reference documentation is built from the `/release/{current released version}` branch (called `/release/x.x` for short in the following).

* If you make simple fixes, you can work on the `/release/x.x` branch and simply push (commit) your changes, and they will be picked up in the next doc build
* If you are making more extensive changes, you should make a branch off of `/release/x.x` and work on that branch.  Push (commit) your changes to your branch to save your work, and when your changes are ready to be integrated into the main doc build, submit a pull request and ask for review

In any case, it's a good idea to create a local build of the doc to check it before you submit your changes to main.  Be sure not to commit the build directory or any of its subcontents.

See the Sphinx markup reference (http://www.sphinx-doc.org/en/stable/markup/index.html) for help understanding how to do more than add text.

**Checking the build logs**

You can always see the local build logs.  If you have access to the Jenkins dashboard (http://dev.dataiku.com/jenkins/), you can look at the Console Output for any build; for example, the logs for the latest build for the 5.1 reference doc is at: http://dev.dataiku.com/jenkins/job/doc-PROD-5.1/lastBuild/console

## Contributing to the developer guide

The developer guide follows the same rules as the refdoc for the branching.
If you want to contribute to the developer guide,
please [read this document](developer-guide/source/_contributions/CONTRIBUTING.md)
(available [online](https://developer.dataiku.com/latest/_contributions/CONTRIBUTING.html))

## Refreshing the third-party credits

The licenses files are generated on the fly by the CI, but not actually committed in this repository.

* Checkout dip (`${DIP_REPOSITORY}), dss-launcher ${DSS_LAUNCHER_REPOSITORY} and dku-story ${DSS_STORIES_REPOSITORY} at the required version

* RUN `DSSLAUNCHERDIR=${DSS_LAUNCHER_REPOSITORY} DSSSTORIESDIR=${DSS_STORIES_REPOSITORY} DKUINSTALLDIR=${DIP_REPOSITORY} make update-licenses`

**Generate the kit's CNF**

Where X.Y = version, with the doc's python environment

```
./generate-cnf.sh
scp dataiku-dss-thirdparty-notice.zip dtkdevadm@dev:/data/dtkdevadm/www/downloads.dataiku.com/htdocs/studio-build/thirdparty-notices/dataiku-dss-thirdparty-notice-X.Y.zip
Update reference in make-studio-package.sh
```

## The pipeline

The pipeline consists of [the multi-branch Jenkins job](https://qa-jenkins.dku.sh/job/Docs/job/DSS-Doc/)
from [the file](./pipeline/Jenkinsfile) that is configured to create a job for each PR
and [the job](https://qa-jenkins.dku.sh/job/Docs/job/RunOnPRDeleteDSSDoc/) from [the file](./pipeline/RunOnPRDelete.Jenkinsfile)
that removes the documentation folder after a PR is closed.

The main job is monitoring this repo and waiting for the PRs that are open and having the _build-docs-on-staging_ label.

The job is using a labeled jenkins machine that is hosting the static html files and running Apache HTTP Server to response the requests.

#### The stages
There are a few parts of the documentations that are built over the corresponding stages:
* Reference documentation and developer guide

  Built on the root of the dss-doc repo and on the developer-guide folder accordingly.
* App-notes

  Built in the app-notes folder of the dss-doc repo.
* R API

  Built in the DIP repo in the [src/main/R/dataiku*](https://github.com/dataiku/dip/tree/master/src/main/R) folders, dataiku.spark* require building and installing the R dataiku library from src/main/R/dataiku. It can be built by running [dip/Makefile](https://github.com/dataiku/dip/blob/master/Makefile) with target R.
* REST API

  Built in the [dip/spec](https://github.com/dataiku/dip/blob/master/spec) folder, by the `make rest`.
* JAVA API

  Built in the [dip/spec](https://github.com/dataiku/dip/blob/master/spec) folder, by the `make java`. Depends on building the dss backed by `make backend` from the [dip/Makefile](https://github.com/dataiku/dip/blob/master/Makefile) upfront.
