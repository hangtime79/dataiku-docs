(wiki)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 25/09/2024
  
  this code samples has been verified on DSS: 14.2.0
  Date of check: 17/09/2025
```

# Wikis

You can interact with the Wiki of each project through the API.

## Getting the DSSWiki object

You must first retrieve the {py:class}`~dataikuapi.dss.wiki.DSSWiki` through the {py:meth}`~dataikuapi.dss.project.DSSProject.get_wiki` method

```python
project = client.get_project("MYPROJECT")
wiki = project.get_wiki()
```

## Retrieving and modifying the content of an article

```python
article = wiki.get_article("article_name")
article_data = article.get_data()

# Modify the content of the article data
current_markdown_content = article_data.get_body()
article_data.set_body("# My new Markdown content")

# And save the modified content
article_data.save()
```

## Deleting an article

```python
article = wiki.get_article("article_name")
article.delete()
```

## Getting the list of all articles

This prints the content of all articles in the Wiki

```python
for article in wiki.list_articles():
        print("Article: %s" % article.article_id)
        article_data = article.get_data()
        print("Content:")
        print(article_data.get_body())
```

## Uploading an attachment to an article

After upload, the attachment can be referenced through the Markdown syntax

```python
article = wiki.get_article("article_name")

with open("/tmp/myimage.jpg", "rb") as f:
        article.upload_attachement(f, "myimage.jpg")

```

## Download an attachment of an article

After being uploaded, the attachment of an article can be retrieved through its upload id

```python
article_metadata = article.get_data().get_metadata()
upload_attachment_id = article_metadata.get('attachments')[0].get("smartId")

attachment_res = article.get_uploaded_file(upload_attachment_id)
```

## Moving an article in the taxonomy

You can change the parent of an article

```python
settings = wiki.get_settings()
settings.move_article_in_taxonomy(article.article_id, parent_article.article_id)
settings.save()
```

## Changing the home article of the wiki

```python
settings = wiki.get_settings()
settings.set_home_article_id(article.article_id)
settings.save()
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataikuapi.dss.wiki.DSSWiki
    dataikuapi.dss.wiki.DSSWikiArticle
    dataikuapi.dss.wiki.DSSWikiArticleData
    dataikuapi.dss.wiki.DSSWikiSettings
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.wiki.DSSWikiArticle.delete
    ~dataikuapi.dss.wiki.DSSWiki.get_article
    ~dataikuapi.dss.wiki.DSSWikiArticleData.get_body
    ~dataikuapi.dss.wiki.DSSWikiArticle.get_data
    ~dataikuapi.dss.wiki.DSSWikiArticleData.get_metadata
    ~dataikuapi.dss.wiki.DSSWiki.get_settings
    ~dataikuapi.dss.wiki.DSSWikiArticle.get_uploaded_file
    ~dataikuapi.dss.project.DSSProject.get_wiki
    ~dataikuapi.dss.wiki.DSSWikiSettings.move_article_in_taxonomy
    ~dataikuapi.dss.wiki.DSSWiki.list_articles
    ~dataikuapi.dss.wiki.DSSWikiArticleData.save
    ~dataikuapi.dss.wiki.DSSWikiArticleData.set_body
    ~dataikuapi.dss.wiki.DSSWikiSettings.set_home_article_id
    ~dataikuapi.dss.wiki.DSSWikiArticle.upload_attachement
```