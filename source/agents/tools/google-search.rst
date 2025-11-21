Google Search Tool
##################


This tool is provided by the "Google Search Tool" plugin, which needs to be installed.

This tool uses Google Custom Search JSON API (also known as Programmable Search Engine) to provide the ability to perform web searches. It is a powerful feature that provides your agent with access to real-time information from the internet, significantly expanding its knowledge base beyond its training data.

To configure the tool, you will need to provide:

- A **Google CustomSearch cx id**: The unique identifier for your Google Programmable Search Engine. This id specifies which engine's configuration to use when performing a search. For instructions, see Google's guide on `Creating a Programmable Search Engine <https://developers.google.com/custom-search/docs/tutorial/creatingcse>`_

- An **API Key**: Your unique API key used to authenticate your application's requests to the Custom Search JSON API. To obtain a key, please refer to the documentation on `Identifying your application to Google <https://developers.google.com/custom-search/v1/introduction#identify_your_application_to_google_with_api_key>`_

Upon a successful query, the tool returns a structured list of search results directly from Google, including titles, links, and snippets for each source.

Please note that this tool requires the agent to have outgoing Internet access.

Test your Google Search tool in the **Quick test**:

.. code-block:: json

    {
        "input": {
            "q": "Your google search query"
        },
        "context": {}
    }
