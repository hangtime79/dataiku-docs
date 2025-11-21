PII detection
##############

PII detection in the LLM Mesh can detect various forms of PII in your prompts and queries, and either block or redact the queries.

Initial setup
==============

You will need a setup with full outgoing Internet connectivity for downloading the models. Air-gapped setups are not supported.


* In "Administration > Code envs > Internal envs setup", in the "PII detection code environment" section, select a Python version in the list and click "Create code environment"
* In "Administration > Settings > LLM Mesh", in the "PII Detection" section, select "Use internal code env"


Enable PII detection 
=====================

Where you want to use the guardrail (either at connection level, agent level or at usage time), select PII Detector and click "Add Guardrail"


You can select whether to:

* Reject queries where PII is detected
* Replace PII by a placeholder, such as "John Smith" -> "<PERSON>"
* Replace PII by a hash value, such as "John Smith" -> "0aa12bc86bd123bd"
* Remove PII, such as "I said hello to John Smith" -> "I said hello to"
* Replace parts of PII by stars, such as "His phone number was (570) 123-4567" -> "His phone number was \********567"

Detected PII types
===================

The following entity types are recognized:

Generic entities:


* CREDIT_CARD
* DATE_TIME
* EMAIL_ADDRESS
* IBAN_CODE
* IP_ADDRESS
* LOCATION
* PERSON
* PHONE_NUMBER
* MEDICAL_LICENSE
* URL

Country-specific entities:

* US_BANK_NUMBER
* US_DRIVER_LICENSE
* US_ITIN
* US_PASSPORT
* US_SSN
* UK_NHS
* ES_NIF
* IT_FISCAL_CODE
* IT_DRIVER_LICENSE
* IT_VAT_CODE
* IT_PASSPORT
* IT_IDENTITY_CARD
* SG_NRIC_FIN
* AU_ABN
* AU_ACN
* AU_TFN
* AU_MEDICARE

Details
========

PII Detection is based on Microsoft Presidio library: https://microsoft.github.io/presidio