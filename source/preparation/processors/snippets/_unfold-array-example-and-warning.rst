
For example, with the following dataset:

+----+-----------------------------+
| id | words                       |
+====+=============================+
|  0 | ['hello', 'hello', 'world'] |
+----+-----------------------------+
|  1 |    ['hello', 'world']       |
+----+-----------------------------+
|  2 |     ['hello']               |
+----+-----------------------------+
|  3 |   ['world', 'world']        |
+----+-----------------------------+

Applying the "Unfold an array" processor on the "words" column will generate the following result:

+----+-----------------------------+-------------+-------------+
| id | words                       | words_hello | words_world |
+====+=============================+=============+=============+
|  0 | ['hello', 'hello', 'world'] |      2      |           1 |
+----+-----------------------------+-------------+-------------+
|  1 |    ['hello', 'world']       |      1      |           1 |
+----+-----------------------------+-------------+-------------+
|  2 |     ['hello']               |      1      |             |
+----+-----------------------------+-------------+-------------+
|  3 |   ['world', 'world']        |             |           2 |
+----+-----------------------------+-------------+-------------+

Each value of the unfolded column will create a new column. This new column:

* contains the number of occurrences of the value found in the original column,
* remains empty if the original column does not contain this value.

.. warning::

	**Limitations**

	The limitations that apply to the :ref:`unfold` processor also apply to the Unfold an array processor. 

