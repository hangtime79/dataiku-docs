Testing a project
#################

To ensure the quality of your project over time, you can test parts of a Dataiku project using dedicated scenario steps (:ref:`Python unit test <python-test-step>`, :ref:`Integration test <flow-test-step>` and :ref:`Webapp test <webapp-test-step>`).

Creating a test scenario
========================

Scenarios have an option to be marked as a :ref:`test scenario <def-test-in-dss>`, which will make them appear in your project's Test Dashboard.

The Test Dashboard displays the status of all the latest test scenario runs.


Test Dashboard
==============

The Test Dashboard is available from the project's Automation Monitoring tab:

* It displays the latest run of test scenarios of the current project (design node) or selected bundle (automation node).
* Each run shows its status, execution date, duration, and quick access to scenario settings, last run view, logs, and scenario/step reports (for pytest steps).
* A summary of run statuses is available.
* Users can manually download a JunitXML report or an HTML report of the Test Dashboard.


Best practices for testing
==========================

This feature is a component that can be used in a wide range of cases, and is dependent on your need, time and requirements. Nonetheless, we can give some generic suggestions:

1. Test scenarios are created on a Design node and can be tested there.
2. You are not limited to dedicated Test steps in these scenarios; they can also use any other scenario step that is relevant in your test execution.
3. Once ready, tests are meant to be executed on a dedicated QA Automation node. This execution can be done manually or automatically (using :ref:`Deployer custom Hooks <deployment-hooks>`, for example).
4. The test report on this QA Automation node can be exported for archiving, but can also be viewed directly on the Automation node and retrieved through the Python API.
5. You can leverage the Test report as part of your deployment process. This can be done through a Custom Hook on your Production infrastructure. You can also push the test report to Dataiku Govern and have it as a resource for :ref:`sign-off <sign-off>`.

.. note::

    If you are interested in building a complete testing pipeline within Dataiku, you can read `our hands-on article in our knowledge base <https://knowledge.dataiku.com/latest/mlops-o16n/test-scenarios/basics/tutorial-index.html>`_.
