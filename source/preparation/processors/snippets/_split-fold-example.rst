For example, with the following dataset:

+-------------+----------------------+---------+
| customer_id |        events        | browser |
+=============+======================+=========+
|           1 | login,product,buy    | Mozilla |
+-------------+----------------------+---------+
|           2 | login,product,logout | Chrome  |
+-------------+----------------------+---------+

Applying "Split and Fold" on the "events" column with ","  as the separator will generate the 
following result:

+-------------+---------+---------+
| customer_id |  events | browser |
+=============+=========+=========+
|           1 | login   | Mozilla |
+-------------+---------+---------+
|           1 | product | Mozilla |
+-------------+---------+---------+
|           1 | buy     | Mozilla |
+-------------+---------+---------+
|           2 | login   | Chrome  |
+-------------+---------+---------+
|           2 | product | Chrome  |
+-------------+---------+---------+
|           2 | logout  | Chrome  |
+-------------+---------+---------+