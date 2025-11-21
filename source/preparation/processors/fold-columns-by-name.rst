.. _fold-multiple-columns:

Fold multiple columns
#############################################

Perform the opposite of a pivot and fold a **list of columns**, transforming a wide dataset into a narrow one. This is also sometimes called a melt. This processor outputs two columns: one containing **column names** and the other containing **column values**. 

Example
=========

=============  =============  =============  =============  
student        math           science        arts 
=============  =============  =============  =============
Marie          85             83             81
Caroline       74             91             86
Paul           70             85             89
=============  =============  =============  =============


Applying “Fold multiple columns” with ``class`` for folded column names and ``grade`` for folded values generates the following table:

=============  =============  =============    
student        class          grade         
=============  =============  =============  
Marie          math           85             
Marie          science        83             
Marie          arts           81 
Caroline       math           74
Caroline       science        91
Caroline       arts           86
Paul           math           70
Paul           science        85
Paul           arts           89            
=============  =============  =============  

Options
=========

**Column for folded column names**

Column containing the names of folded columns.

**Column for folded values**

Column containing the values of folded columns.

**Remove folded columns**

Remove the now empty folded columns.

Related resources
===================

For more information, read about `reshaping data <https://doc.dataiku.com/dss/11.0/preparation/reshaping.html>`__ in the Dataiku documentation. 
