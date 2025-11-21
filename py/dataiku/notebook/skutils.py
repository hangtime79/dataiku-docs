import StringIO

from sklearn.tree import _tree
import random

def dataframe_train_test_split(size, X, Y):
    ## sklearn.cross_validation would not respect X / Y original index
    if type(size) != int:
        size = int (len(X.index) * size)

    test_index = random.sample(X.index, size)
    return X.drop(test_index), X.ix[test_index], Y.drop(test_index), Y.ix[test_index]


def dtype_valid_for_ml(d):
    return d.kind in "bfi"

def dataframe_copy(df): 
    df2 = df.copy()
    if hasattr(df, 'name'):
        df2.name = df.name
    return df2

def prepare_for_ml(dataset, copy=True):
    if copy: 
        X = dataframe_copy(dataset)
    else:
        X = dataset
    for c in X.dtypes.index:
        if not dtype_valid_for_ml(X.dtypes[c]):
            del X[c]
    return X


def display_tree(tree, Xtrain, YTrain):
    from IPython.display import Image, display
    import pydot
    dot_data = StringIO.StringIO()


    classes_names = YTrain.unique()

    if len(classes_names) == 2:
        classes_names = ['not_' + YTrain.name, YTrain.name]

    export_graphviz(tree, out_file = dot_data, feature_names=Xtrain.columns, classes_names=classes_names, max_depth=4)
#    s = dot_data.getvalue()
#    s = re.sub(r"value = \[\s+(\d+)\.\s+(\d+)\.\]", lambda m:  "fragile = %2.f%%" % (100*float(m.group(2)) / (float(m.group(2)) + float(m.group(1)))), s) 
#   print s 
    graph = pydot.graph_from_dot_data(str(dot_data.getvalue())) 
    display(Image(graph.create_png()))


def export_graphviz(decision_tree, out_file="tree.dot", feature_names=None, classes_names=None,
                    max_depth=None, close=True):


    def isbinary_node(tree, node_id):
        return tree.threshold[node_id] == 0.5


    def classes_to_str(value):
        s = sum(value)
        percents = [float(v) * 100  / s for v in value]
        if len(classes_names) == 2:
            mvalue = max(percents)
            mclass = classes_names[percents.index(mvalue)]
            return "%s (%2.f%%)" % (mclass, mvalue)
        else: 
            percents_string = ["%s:%2.f%%"  % (k, v) for k, v in zip(classes_names, percents) if int(v) > 0]
            return ",".join(percents_string)

    def node_to_str(tree, node_id):
        value = tree.value[node_id]
        if tree.n_outputs == 1:
            value = value[0, :]

        if isinstance(tree.criterion, _tree.Gini):
            criterion = "gini"
        elif isinstance(tree.criterion, _tree.Entropy):
            criterion = "entropy"
        elif isinstance(tree.criterion, _tree.MSE):
            criterion = "mse"
        else:
            criterion = "impurity"

        if tree.children_left[node_id] == _tree.TREE_LEAF:
            return "samples = %s\\n%s" \
                   % (#criterion,
                      #tree.init_error[node_id],
                      tree.n_samples[node_id],
                      classes_to_str(value))
        else:
            if feature_names is not None:
                feature = feature_names[tree.feature[node_id]]
            else:
                feature = "X[%s]" % tree.feature[node_id]

            if isbinary_node(tree, node_id):
                return "%s ?\\nsamples = %s\\n%s" \
                       % (feature,
                          #criterion,
                          #tree.init_error[node_id],
                          tree.n_samples[node_id],
                          classes_to_str(value))
            else:

                return "%s <= %.4f\\nsamples = %s\\n%s" \
                       % (feature,
                          tree.threshold[node_id],
                          #criterion,
                          #tree.init_error[node_id],
                          tree.n_samples[node_id],
                          classes_to_str(value))

    def recurse(tree, node_id, parent=None, depth=0):
        if node_id == _tree.TREE_LEAF:
            raise ValueError("Invalid node_id %s" % _tree.TREE_LEAF)

        left_child = tree.children_left[node_id]
        right_child = tree.children_right[node_id]

        # Add node with description
        if max_depth is None or depth <= max_depth:
            out_file.write('%d [label="%s", shape="box"] ;\n' %
                           (node_id, node_to_str(tree, node_id)))

            if parent is not None:
                # Add edge to parent
                out_file.write('%d -> %d ;\n' % (parent, node_id))

            if left_child != _tree.TREE_LEAF:
                recurse(tree, left_child, parent=node_id, depth=depth + 1)
                recurse(tree, right_child, parent=node_id, depth=depth + 1)

        else:
            out_file.write('%d [label="(...)", shape="box"] ;\n' % node_id)

            if parent is not None:
                # Add edge to parent
                out_file.write('%d -> %d ;\n' % (parent, node_id))

    #if isinstance(out_file, six.string_types):
    #    if six.PY3:
    #        out_file = open(out_file, "w", encoding="utf-8")
    #    else:
    #        out_file = open(out_file, "wb")

    out_file.write("digraph Tree {\n")
    if isinstance(decision_tree, _tree.Tree):
        recurse(decision_tree, 0)
    elif hasattr(decision_tree, "tree_"):
        recurse(decision_tree.tree_, 0)
    elif hasattr(decision_tree, "estimators_"):
        imps = [ decision_tree.feature_importances_[est.tree_.feature[0]] for est in decision_tree.estimators_]
        i = imps.index(max(imps))
        recurse(decision_tree.estimators_[i].tree_, 0)
    else:
        raise Exception("Cannot display has a tree")
    out_file.write("}")

    return out_file