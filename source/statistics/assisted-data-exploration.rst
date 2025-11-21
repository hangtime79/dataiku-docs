Assisted Data Exploration
#########################

It can sometimes be difficult to readily spot patterns and relationships in a
dataset, especially if there are many columns or if you don't already have
some notion of where to begin your analysis.

Dataiku provides an assistant to ease the exploration of datasets. When
creating a new card, you can choose "Automated Selection", which helps you
discover patterns by suggesting analyses on variables of interest.

The tool gathers metrics about the current sample and makes card suggestions
based on the selected variables. Suggestions evolve as you select or unselect
variables, and cover all the interactive statistics cards currently supported
by Dataiku.

Suggestions can be previewed, selected and then added to the current worksheet.

.. image:: img/assisted-exploration.png

.. note::
    All calculations made by the assistant are performed on a subset of 1000
    points randomly drawn from the sample of the worksheet. As a consequence,
    suggested card thumbnails may not reflect the actual content of the card
    and are provided as visual indications only. In order to get reliable
    results, it is advised to preview the card first, as previews are always
    computed on the whole sample of the worksheet.
