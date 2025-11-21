JSON
############

The JavaScript Object Notation is a concise, versatile and textual format, used for handling any object structure. This format is used by a wide range of applications, even for large amounts of data. MongoDb, for example, can store data as JSON.

Data in JSON format can come under two flavors: either as a concatenation of JSON objects, or as as an array of JSON objects. Data Science Studio assumes the former, but can handle the latter when provided with the name of the field holding the array. The combination of both types is not handled directly in the dataset settings, though. In the case of records located in the arrays of concatenated JSON objects, Data Science Studio must first read the concatenated objects, then use a recipe to extract the arrays then the objects then fold the objects of the array.

Since arrays in JSON can be deeply nested, it is in some cases convenient to flatten them directly upon ingesting the data. Data Science Studio can flatten arrays while controlling how many unflattened objects are created, in order not to create too many columns in the dataset.

Example
~~~~~~~~~

Flattening arrays with a limit of 2 on the index of flattened elements

Input::

    {
    	"system": "RGB",
    	"colors": ["red","green","blue"]
    }
    {
    	"system": "CYMK",
    	"colors": ["cyan","yellow","magenta","key"]
    }

Output:

+--------+----------+----------+----------+
| system | colors.0 | colors.1 | colors.2 |
+========+==========+==========+==========+
| RGB    | red      | green    | blue     |
+--------+----------+----------+----------+
| CYMK   | cyan     | yellow   | magenta  |
+--------+----------+----------+----------+
