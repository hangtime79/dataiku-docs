
For example, with the following dataset:


+-------------+------------------------+
| customer_id |         events         |
+=============+========================+
|           1 | login, product, buy    |
+-------------+------------------------+
|           2 | login, product, logout |
+-------------+------------------------+

We get:

+-------------+--------------+----------------+------------+---------------+
| customer_id | events_login | events_product | events_buy | events_logout |
+=============+==============+================+============+===============+
|           1 |            1 |              1 |          1 |               |
+-------------+--------------+----------------+------------+---------------+
|           2 |            1 |              1 |            |             1 |
+-------------+--------------+----------------+------------+---------------+

The unfolded column is deleted.

.. warning::

	**Limitations**

	The limitations that apply to the :ref:`unfold` processor also apply to the Split and Unfold processor.
