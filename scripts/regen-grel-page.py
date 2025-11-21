import json
import sys

json_file = sys.argv[1]
rst_file = sys.argv[2]

page_header="""
FORMULA TO BE INTEGRATED
##########################
"""

def dump_function(f, function):
        if function.get('hideFromDocumentation', False) == True:
                return
        header = '%s(%s) *%s*' % (function['name'], function.get('params', ''), function.get('returns', ''))
        f.write(header)
        f.write('\n')
        f.write('-' * len(header))
        f.write('\n')
        f.write('\n')
        f.write(function.get('documentation', function.get('description', '')))
        f.write('\n')
        f.write('\n')

def dump_category(f, category):
        header = category['name']
        if len(header) > 0:
                f.write(header)
                f.write('\n')
                f.write('=' * len(header))
                f.write('\n')
                f.write('\n')
        for function in category['functions']:
                dump_function(f, function)


package_to_category = {u'com.google.refine.expr.functions.math':'Math functions'
                      ,u'com.google.refine.expr.functions.strings':'String functions'
                      ,u'com.google.refine.expr.functions.booleans':'Boolean functions'
                      ,u'com.google.refine.expr.functions.date':'Date functions'
                      ,u'com.google.refine.expr.functions':'Functions'
                      ,u'com.google.refine.expr.functions.arrays':'Array functions'
                      ,u'com.google.refine.expr.functions.html':'Object functions'}

def get_category(function):
        category = function.get(u'category', 'Functions')
        if category in package_to_category:
                category = package_to_category[category]
        return category

def group_by_category(functions):
        def function_cmp(a,b):
                a_category = get_category(a)
                b_category = get_category(b)
                if a_category < b_category:
                        return -1
                if a_category > b_category:
                        return 1
                return cmp(a['name'], b['name'])
        functions = sorted(functions, cmp=function_cmp)

        categories = []
        last_category = None
        for function in functions:
                category_name = get_category(function)
                if last_category is None or last_category['name'] != category_name:
                        if last_category is not None:
                                categories.append(last_category)
                        last_category = {'name' : category_name, 'functions' : []}
                last_category['functions'].append(function)
        if last_category is not None:
                categories.append(last_category)

        return categories


with open(json_file, 'r') as f:
        grel_functions = json.load(f)

print('Got %i functions from DSS' % len(grel_functions))

with open(rst_file, 'w') as f:
        f.write(page_header)
        for category in group_by_category(grel_functions):
                dump_category(f, category)
