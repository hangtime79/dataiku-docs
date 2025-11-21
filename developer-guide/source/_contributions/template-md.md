```{eval-rst}
:orphan:
```

# Template for writing a tutorial (Your title here)
 
## Prerequisites
* Dataiku version, a disclaimer if the tutorial doesn't work on Dataiku Cloud
* User permissions (both connection and project level)
* Python version and packages version
* Expected initial state, e.g.:
  * existing project
  * dataset
  * models
  * knowledge

## Introduction/context (you can change the title if you need)
What problems solve in your tutorial?

## Step 1

### Sub-step if needed.

## Step 2

## .../...

## Complete code (if applicable)

## Wrapping up/Conclusion

## Reference documentation

### Classes
```{eval-rst}
.. autosummary::
  dataikuapi.DSSClient
```

### Functions
```{eval-rst}
.. autosummary::
  ~dataikuapi.DSSClient.get_default_project
```
