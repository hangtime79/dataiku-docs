(meanings)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 25/09/2024
  
  this code samples has been verified on DSS: 14.2.0
  Date of check: 18/09/2025
```
# Meanings

The API offers methods to retrieve the list of meanings and their definition, to create a new meaning or update an existing one.

## Listing meanings

The list of all user-defined meanings can be fetched with the {py:meth}`~dataikuapi.DSSClient.list_meanings()` method of the {py:class}`~dataikuapi.DSSClient`.

```python
client.list_meanings()
```

## Creating a meaning

The {py:meth}`dataikuapi.DSSClient.create_meaning` method can be used to create new meanings.

```python
# Creating a declarative meaning
client.create_meaning("meaning_1", "Test meaning", "DECLARATIVE",
        description="Test meaning description"
)

# Creating a value list meaning
client.create_meaning("meaning_2", "Test meaning", "VALUES_LIST",
        description="Test meaning",
        values=["mercury","venus","earth","mars","jupiter","saturn","uranus","neptune"],
        normalizationMode="LOWERCASE"
)

# Creating a value mapping meaning
client.create_meaning("meaning_3", "Test meaning", "VALUES_MAPPING",
        mappings=[
                {"from": "0", "to": "no"   },
                {"from": "1", "to": "yes"  },
                {"from": "2", "to": "maybe"}
        ]
)

# Creating a pattern meaning
client.create_meaning("meaning_4", "Test meaning", "PATTERN", pattern="[A-Z]+")
```

## Editing a meaning

Existing meanings can be fetched by calling the {py:meth}`dataikuapi.DSSClient.get_meaning` method with the meaning ID. It returns a meaning handle that can be used to get or set the meaning's definition with {py:meth}`~dataikuapi.dss.meaning.DSSMeaning.get_definition` and {py:meth}`~dataikuapi.dss.meaning.DSSMeaning.set_definition`, as follows:

```python
meaning = client.get_meaning("meaning_1")
definition = meaning.get_definition()
definition['label'] = "New label"
definition['description'] = "New description"
meaning.set_definition(definition)
```

## Assigning a meaning to a column

Meanings can be assigned to columns by editing the schema of their dataset and setting the ``meaning`` field of the column to the ID of the desired meaning.

```python
dataset = client.get_project("TEST_PROJECT").get_dataset("TEST_DATASET")
schema = dataset.get_schema()
schema['columns'][2]['meaning'] = "meaning_1"
dataset.set_schema(schema)
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataikuapi.dss.meaning.DSSMeaning
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.DSSClient.create_meaning
    ~dataikuapi.dss.meaning.DSSMeaning.get_definition
    ~dataikuapi.DSSClient.get_meaning
    ~dataikuapi.DSSClient.list_meanings
    ~dataikuapi.dss.meaning.DSSMeaning.set_definition
```