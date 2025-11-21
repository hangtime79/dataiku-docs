(discussions)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 25/09/2024
  
  this code samples has been verified on DSS: 14.2.0
  Date of check: 17/09/2025
```

# Discussions

You can interact with the discussions on each DSS object through the API.

## Obtaining the discussions

The first step is always to retrieve a {py:class}`~dataikuapi.dss.discussion.DSSObjectDiscussions` object corresponding to the DSS object your manipulating. 
Generally, it's through a method called `get_object_discussions`

```python
# Get the discussions of a dataset
discussions = dataset.get_object_discussions()

# Get the discussion of a wiki article
discussions = wiki.get_article("my article").get_object_discussions()

# Get the discussions of a project
discussions = project.get_object_discussions()

# ...
```

## List the discussions of an object

```python
for discussion in discussions.list_discussions():
        # Discussion is a DSSDiscussion object
        print("Discussion with id: %s" % discussion.discussion_id)
```

## Reading the messages of a discussion

```python
for message in discussion.get_replies():
        print("Message by author %s" % message.get_author())
        print("Message posted on %s" % message.get_timestamp())
        print("Message content: %s" % message.get_text())
```

## Adding a new message to a discussion

```python
discussion.add_reply("hello world\n# This is Markdown")
```

## Creating a new discussion

```python
new_discussion = discussions.create_discussion("Topic", "Hello, this is the message")
```

## Detailed examples

This section contains more advanced examples on discussions.

### Export discussions from a Project

You can programmatically retrieve all discussion messages from various "commentable" items in a Project.

```{literalinclude} examples/discussions/export-from-project.py
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataikuapi.dss.discussion.DSSDiscussion
    dataikuapi.dss.discussion.DSSDiscussionReply
    dataikuapi.dss.discussion.DSSObjectDiscussions
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.discussion.DSSDiscussion.add_reply
    ~dataikuapi.dss.discussion.DSSObjectDiscussions.create_discussion
    ~dataikuapi.dss.discussion.DSSDiscussionReply.get_author
    ~dataikuapi.dss.dataset.DSSDataset.get_object_discussions
    ~dataikuapi.dss.project.DSSProject.get_object_discussions
    ~dataikuapi.dss.wiki.DSSWikiArticle.get_object_discussions
    ~dataikuapi.dss.discussion.DSSDiscussion.get_metadata
    ~dataikuapi.dss.discussion.DSSDiscussion.get_replies
    ~dataikuapi.dss.discussion.DSSDiscussionReply.get_timestamp
    ~dataikuapi.dss.discussion.DSSDiscussionReply.get_text
    ~dataikuapi.dss.discussion.DSSObjectDiscussions.list_discussions
```