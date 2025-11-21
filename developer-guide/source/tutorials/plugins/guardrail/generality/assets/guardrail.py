# This file contains the implementation of the custom guardrail devadv-tutorial
import logging
import dataiku
from dataiku.llm.guardrails import BaseGuardrail


class CustomGuardrail(BaseGuardrail):
    def set_config(self, config, plugin_config):
        self.usesInstructions = config.get('usesInstructions')
        self.instructions = config.get('instructions', '')
        self.rewriteAnswer = config.get('rewriteAnswer')
        self.llm = config.get('llm', 'openai:toto:gpt-4o-mini')
        self.extraFormatting = config.get('extraFormatting', '')

    def process(self, input, trace):
        logging.info("[------ GUARDRAIL PLUGIN -------------]")

        if self.rewriteAnswer and ("completionResponse" in input):
            logging.info("[-------- PLUGIN GUARDRAIL --------]: --> %s" % input["completionResponse"]["text"])
            with trace.subspan("Devadvocate Guardrail Plugin") as sub:
                logging.info("[-------- PLUGIN GUARDRAIL -------- SUB --------]")
                llm = dataiku.api_client().get_default_project().get_llm(self.llm)
                resp = llm.new_completion().with_message("This is the answer: %s --- %s" % (
                    input["completionResponse"]["text"], self.extraFormatting)).execute()
                sub.append_trace(resp.trace)
                if resp.success:
                    input["completionResponse"]["text"] = resp.text
        elif self.usesInstructions and ("completionQuery" in input):
            # do any processing and decide on an action here
            question = input["completionQuery"]["messages"]
            question[0]["content"] = "%s %s" % (question[0]["content"], self.instructions)
            input["completionQuery"]["messages"] = question
        return input
