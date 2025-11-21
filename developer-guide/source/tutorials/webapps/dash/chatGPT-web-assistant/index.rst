Using Dash and LLM Mesh to build a GPT-powered web app assistant
**********************************************************************

Prerequisites
#############

* Dataiku >= 13.0
* "Use" permission on a code environment using Python >= 3.9 with the following packages:
    * ``dash`` (tested with version ``2.10.2``)
    * ``dash-bootstrap-components`` (tested with version ``1.4.1``)
* Access to an existing project with the following permissions:
    * "Read project content"
    * "Write project content"

Introduction
############

In this tutorial, you will learn to call a GPT model into a Dataiku web app for a simple
question-answering task.

LLM initialization and library import
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To begin with, you need to set up a development environment
by importing some necessary libraries and initializing the chat LLM you want to use.
The tutorial relies on the LLM Mesh for this.

.. tip::

    The :ref:`documentation<ce/llm-mesh/get-llm-id>` provides instructions on obtaining an ``LLM ID``.
    The following code snippet will print you an exhaustive list of all the models your project has access to.

    .. code-block:: python
        :caption: Code 1: List accessible LLM

        import dataiku
        client = dataiku.api_client()
        project = client.get_default_project()
        llm_list = project.list_llms()
        for llm in llm_list:
            print(f"- {llm.description} (id: {llm.id})")


Using the prompt through the LLM Mesh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To check if everything is working as expected, you can run :ref:`Code 2<tutorial_webapp_dash_chatgpt_test_notebook>` in a notebook.

.. code-block:: python
    :name: tutorial_webapp_dash_chatgpt_test_notebook
    :caption: Code 2: Code for testing if all requirements are met.

    LLM_ID = "" # Replace with a valid LLM id

    # Get a text generation model
    llm = project.get_llm(LLM_ID)

    # Create and run a completion query
    completion = llm.new_completion()
    completion.with_message("Write a haiku on GPT models")
    resp = completion.execute()

    # Display the LLM output
    if resp.success:
       print(resp.text)

Building the web app
####################

CSS file
^^^^^^^^
Before sketching the web app, you must create an accessible CSS file.
Go to the **Application menu > Global Shared Code > Static web resources**.
Create a file named ``loading-state.css`` inside the ``local-static`` directory, with the content shown in
:ref:`Code 3<tutorial_webapp_dash_chatgpt_webapp_css>`.
As shown in the next section, this code will help display an indicator when you query the model.

.. literalinclude:: ./assets/loading-state.css
    :language: css
    :caption: Code 3: CSS code for indication of a loading state
    :name: tutorial_webapp_dash_chatgpt_webapp_css

Sketching the Webapp
^^^^^^^^^^^^^^^^^^^^
First, you need to create an empty Dash webapp. If you don't know how to create one, please refer to this
:doc:`mini-tutorial<../common-parts/create-the-webapp-empty-template>`.

Then, import all the required libraries and configure the webapp to use the CSS file you created.
:ref:`Code 4<tutorial_webapp_dash_chatgpt_dash_import>` shows how to do this.

.. literalinclude:: ./assets/webapp.py
    :language: python
    :caption: Code 4: Import packages
    :name: tutorial_webapp_dash_chatgpt_dash_import
    :lines: 1-12,53-55

Now, you can design the application. You will need a user input and a chatGPT output for this application.
As the webapp focuses on a question-answering bot, you should keep some context (the previously asked questions
and answers).
You must limit the context size to avoid long queries and reduce costs.
There are various ways to do that, but the most understandable is restricting the messages kept by a certain amount.
Usually, OpenAI uses a token counter to do that, but it is not a human-readable metric.
You also may need a button to reset the conversation if the user needs it.

To sum up, we need the following:

* a number input (for the size of the kept messages)
* a button to reset the conversation
* a text input (for the user input)
* a text to display the response.


:ref:`Code 5<tutorial_webapp_dash_chatgpt_webapp_layout>` implements this application.
The highlighted line is where the application will display a processing spinner when the user sends its request.
This line works in conjunction with the CSS defined earlier.

.. literalinclude:: ./assets/webapp.py
    :language: python
    :caption: Code 5: Design of the application.
    :name: tutorial_webapp_dash_chatgpt_webapp_layout
    :lines: 56-79,83-84
    :emphasize-lines: 15

Now that you have designed the application, you only have to connect the components and call the associated functions.
The first highlighted line in :ref:`Code 6<tutorial_webapp_dash_chatgpt_webapp_callbacks>` is the callback associated
with the Q&A processing. The second one resets the current conversation.

.. literalinclude:: ./assets/webapp.py
    :language: python
    :name: tutorial_webapp_dash_chatgpt_webapp_callbacks
    :caption: Code 6: Callbacks of the webapp
    :lines: 91-153
    :emphasize-lines: 14,53

Saving the response into a dataset
##################################

Requesting GPT assistance might be costly, so you could create your cache
and save the question that has already been answered and its response.
So, before requesting an answer from the GPT assistant, check if the question has been asked.
If so, reply with the previous response or ask the GTP assistant if the question has yet to be asked.
Depending on the dataset type, adding data to an existing dataset could be done in various ways.
Let's consider two kinds of datasets:

* For an SQL-like dataset, you can then use the :class:`dataiku.SQLExecutor2` to insert data into a dataset.
* For a CSV-like dataset, you can then load the data as a dataframe, add data and save back the dataframe.
  This method requires loading the whole dataset into memory and may be inappropriate for big datasets.

You first need to create one to save the answers in a dataset.
This dataset must have been defined before, with two columns named ``question`` and ``answer``.

Adding a button to save the data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Before digging into the details,
you should add a button to the webapp allowing the user to save the question and the answer into a dataset.
This is done in two steps:

* First, add a save button to the layout:
    .. code-block:: python
        :caption: Code 7: Adding a button for saving the Q&A
        :name: tutorial_webapp_dash_chatgpt_webapp_additional_button

        dbc.Row([dbc.Col(dbc.Button("Save this answer",
                                    id="save_answer",
                                    n_clicks=0,
                                    class_name="btn-primary",
                                    size="lg"))],
                justify="end",
                className="d-grid gap-2 col-12 mx-auto", )

* Then connect this button to a callback in charge of saving the Q&A:
    .. code-block:: python
        :caption: Code 8: Connecting the button to a callback
        :name: tutorial_webapp_dash_chatgpt_webapp_callbacks_2

        @app.callback(
            Output("save_answer", "n_clicks"),
            Input("save_answer", "n_clicks"),
            State("search_input", "value"),
            State("text_output", "value"),
            prevent_initial_call = True
        )
        def save_answer(_, question, answer):




Depending on the dataset kind, the implementation of the callback will change.

Using the SQLExecutor
^^^^^^^^^^^^^^^^^^^^^
Considering you already have an SQL dataset, you can use the SQLExecutor to insert a row into a dataset,
letting the dataset engine optimize for you. To insert a new row, you will need to use an INSERT statement,
like ``sql = f"""INSERT INTO "{table_name}" (question, answer) VALUES {values_string}"""``.
You may face trouble using this kind of statement if the answer contains some specific characters (like ', ", ...).
As you have no control of the response
(and fine-tuning the prompt might be tough to prevent the assistant from generating an appropriate answer),
you must encode the response before inserting it into the dataset into a proper format.

:ref:`Code 10<tutorial_webapp_dash_chatgpt_webapp_saving_sql>` shows how to encode the question
and the response before inserting the data using the SQL statement and the :class:`dataiku.SQLExecutor2`.

.. code-block:: python
    :caption: Code 9: Saving the data into a SQL-Like dataset
    :name: tutorial_webapp_dash_chatgpt_webapp_saving_sql

    def write_question_answer_sql(client, dataset_name, connection, connection_type, project_key, question, answer):
        dataset = dataiku.Dataset(dataset_name)
        table_name = dataset.get_location_info().get('info', {}).get('table')
        value_string = (f"('{base64.b64encode(question.encode('utf-8')).decode('utf-8')}', "
                        f"'{base64.b64encode(answer.encode('utf-8')).decode('utf-8')}')")
        sql = f"""INSERT INTO "{table_name}" (question, answer) VALUES {value_string}"""
        client.sql_query(sql, connection=connection, type=connection_type, project_key=dataset.project_key,
                         post_queries=['COMMIT'])


Using dataframe
^^^^^^^^^^^^^^^
If your dataset fits into memory, you can rely on the dataframe to append the data to an existing CSV-like dataset.
The principle is straightforward:

* Read the dataset as a dataframe.
* Create the data.
* Append them to the dataframe.
* Save back the dataframe.

Code 10 shows how to do this.

.. code-block:: python
    :caption: Code 10: Saving the data into a CSV-Like dataset
    :name: tutorial_webapp_dash_chatgpt_webapp_saving_csv

    def write_question_answer_csv(dataset_name, question, answer):
        dataset = dataiku.Dataset(dataset_name)
        row = {
            "question": [f"""{question}"""],
            "answer": [f"""{answer}"""]
        }
        df = dataset.get_dataframe()
        df = pd.concat([df, pd.DataFrame(row)])
        with dataset.get_writer() as writer:
            writer.write_dataframe(df)



.. note::

    Dataiku offers an optional response cache in the LLM Mesh connections, but it keeps data for 24 hours, with a 1GB limit.


Wrapping up
###########

Congratulations!
You have completed this tutorial and built a Dash web application that enables ChatGPT integration
inside a Dataiku webapp.
Understanding all these basic concepts allows you to create more complex applications.

You can add a field to this web application to tweak the way Chat GPT answers or try to reduce the number of tokens
used in a query.
If you save the data into a dataset, you can look for the question before requesting the ChatGPT assistant.

In this web application, you keep a fixed number of messages.
When this number is reached, you remove the first message.
Keeping only a specified number of messages in the conversation is not the best idea.
You should rather implement a mechanism that sums up the conversation
and keep this summary as the content of the first message.
An LLM can do this for you.


Here is the complete code for your application:

.. dropdown:: :download:`webapp.py<./assets/webapp.py>`

    .. literalinclude:: ./assets/webapp.py
        :language: python



.. dropdown:: :download:`loading-state.css<./assets/loading-state.css>`

    .. literalinclude:: ./assets/loading-state.css
        :language: CSS

