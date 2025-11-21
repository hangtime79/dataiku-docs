# HOWTO: Create a Sublicense without using Cloud Stacks

If you have a license with 100 users, but have 4 independent groups within the company, and each has purchased 25 licenses, you want each group to be limited to these 25 licenses, rather than giving to each of them the license with 100 users, which requires you to track users among all instances.

This is natively managed in Cloud Stacks using the "sublicense" option. This app note shows how to create a sublicense without Cloud Stacks

* Make a backup of your license.json file

* At the end of the file, add a "sublicense" section

    ```
    {
        "content": {
            "licensee": {
                "company": "...",
                "name": "...
            },
            "properties": {
                "some": "data",

                "maxDesigners": 100,
                "maxReaders": 2000
            },
            "expiresOn": "20221030"
        },
        "r1Sig": "a long signature",
        "r1Pub": "another long signature",
        "r1PubSig": "yet another long signature",

        "sublicense": {
            "profileLimits": {
                "DESIGNER": 25,
                "READER": 100
            }
        }
    }
    ```

* Use this modified license.json file for your instance. The instance can now only have 25 designers and 100 readers (instead of 100 designers and 2000 readers)


Sublicenses are a cooperative mechanism. It is not technically impossible for the administrator of the group who receives the sublicense to alter it. Doing so could however put you in breach of your Dataiku License Agreement.