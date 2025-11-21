Project Setup
=============

What is Project Setup?
----------------------

As a project administrator, Project Setup allows to create a project configuration wizard: a guided, structured workflow to help users finish configuring a project so that it becomes ready to use.

Then, when opening for the first time a project with a Project Setup, DSS users with appropriate permissions can walk through the guided setup and perform necessary configuration tasks, ensuring that all critical steps are completed before the project can be effectively utilized.

Once configured, the Project Setup presents users with organized sections containing specific actions they need to perform, such as uploading datasets, configuring connections, setting variables, or running initial scenarios. This guided approach both reduces the complexity and ensures the consistency of project onboarding.

Restrictions
------------

* **Reader Profile**: Users with Reader profile cannot access or use Project Setup functionality whereas they are able to access Dataiku Applications.
* **Project Application**: Project Setup is not available for projects that have been converted into a Dataiku Application (Visual Application or Application-as-recipe).
* **Feature usage frequency**: The Project Setup UI is not intended for daily usage. It is designed as a one-time or occasional configuration tool, not for routine project operations.
* **Project duplication/export/import**: When duplicating, exporting, or importing a project that already has a completed setup, the setup configuration is copied along with the project. This may not align with end user expectations, as the new project instance may not require the same setup steps or may need different configuration values.

When to Use Project Setup vs. Dataiku Applications
---------------------------------------------------

Project Setup is ideal to create a project template that can be reused with different configurations. It's particularly useful when users need to perform one-time setup tasks like running scenarios, variable configuration, or initial data uploads, and to ensure consistent project configuration across different environments.

Dataiku Applications are better suited to provide ongoing, interactive functionality to end users, when Reader profiles need access to the functionality, when the solution requires regular user interaction rather than one-time setup, or to create a simplified interface for routine project operations.

Key Differences:
~~~~~~~~~~~~~~~~

* **Audience**: Project Setup targets project configurators and administrators; Dataiku Applications target end users including those with Reader profiles
* **Frequency**: Project Setup is for one-time or occasional configuration; Dataiku Applications are for regular usage
* **Purpose**: Project Setup ensures proper project configuration; Dataiku Applications provide simplified interfaces for project functionality (Visual Applications or Application-as-recipe)

Adding Project Setup to an Existing Project
--------------------------------------------

To add Project Setup to an existing project:

1. **Access Application Designer**
   
   * Go to your project's main page
   * Click on the ``...`` (more actions) menu
   * Select "Application Designer"

2. **Enable Project Setup**
   
   * In the Application Designer, click "Show advanced options"
   * Click "Add a setup action to this project"

3. **Create Setup Sections**
   
   * Add sections to organize related configuration tasks in the logical order users should complete them
   * Give each section a pertinent name and optional description

4. **Configure Actions**
   
   * Within each section, add specific actions users need to perform
   * Choose from available action types ("Upload files in dataset", "Edit datasets", "Configure variables", etc.)
   * Provide clear titles for each action
   * Re-organize actions by dragging within a section if necessary

5. **Usage**
   
   * Save your Project Setup configuration
   * Duplicate the project containing the Project Setup configuration to share copies with users
   * Users will see the setup interface when they access the duplicated project

Once configured, Project Setup will be available on the duplicated project's homepage. Users will see a message that says "This project requires setup" with a project setup button to start the guided configuration flow.