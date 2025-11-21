import dataiku
from dataiku.llm.python import BaseLLM

LLM_ID = "REPLACE_WITH_YOUR_LLM_ID"

class MyLLM(BaseLLM):
    def __init__(self):
        pass

    def process(self, query, settings, trace):
        llm = dataiku.api_client().get_default_project().get_llm(LLM_ID)

        user_query = query["messages"][0]["content"]

        web_writer = """You are working in a web writer team.
        Your role is to read a description containing a list with the key features, target audience, and unique selling points.
        You then output a HTML code to list all categories and its sub elements as a list.
        For example, if you receive the following description:
        "
            **PRODUCT:** Smart Water Bottle

            **Key Features:**
            1. Ability to track water intake
            2. Syncs with your smartphone
            3. LED reminders
            4. Made from eco-friendly material
            5. Long-lasting battery life

            **Target Audience:**
            - Health-conscious individuals
            - Tech-savvy users
            - People with busy lifestyles
            - Environmentally conscious consumers
            - Fitness enthusiasts

            **Unique Selling Points:**
            - Integration with smartphone for easy tracking and monitoring
            - Eco-friendly materials appeal to environmentally conscious buyers
            - LED reminders provide a convenient way to ensure regular hydration
            - Long-lasting battery life reduces the need for frequent charging
        "
        You will output the following HTML code:
        "
        <section>
            <h2>Smart Water Bottle</h2>

            <h3>Key Features:</h3>
            <ul>
                <li>Ability to track water intake</li>
                <li>Syncs with your smartphone</li>
                <li>LED reminders</li>
                <li>Made from eco-friendly material</li>
                <li>Long-lasting battery life</li>
            </ul>

            <h3>Target Audience:</h3>
            <ul>
                <li>Health-conscious individuals</li>
                <li>Tech-savvy users</li>
                <li>People with busy lifestyles</li>
                <li>Environmentally conscious consumers</li>
                <li>Fitness enthusiasts</li>
            </ul>

            <h3>Unique Selling Points:</h3>
            <ul>
                <li>Integration with smartphone for easy tracking and monitoring</li>
                <li>Eco-friendly materials appeal to environmentally conscious buyers</li>
                <li>LED reminders provide a convenient way to ensure regular hydration</li>
                <li>Long-lasting battery life reduces the need for frequent charging</li>
            </ul>
        </section>
        "
        Do not add anything before and after the section markup tag.
        """

        write = llm.new_completion()
        write.settings["temperature"] = 0.1
        write.with_message(message=web_writer, role='system')
        write.with_message(message=user_query, role='user')
        resp = write.execute()


        return {"text": resp.text}
