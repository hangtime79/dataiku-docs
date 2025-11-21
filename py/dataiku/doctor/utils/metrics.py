import numpy as np
from sklearn.metrics import roc_auc_score


def log_loss(y_true, y_pred, eps=1e-15, normalize=True):
    """Log loss, aka logistic loss or cross-entropy loss.

    sk-learn version is bugged when a class
    never appears in the predictions.
    """
    (nb_rows, nb_classes) = y_pred.shape
    assert y_true.shape == (nb_rows,)
    assert y_true.max() <= nb_classes - 1
    Y = np.clip(y_pred, eps, 1 - eps)
    Y /= Y.sum(axis=1)[:, np.newaxis]
    T = np.zeros((nb_rows, nb_classes))
    for r in xrange(nb_rows):
        T[r, int(y_true[r])] = 1.
    loss = -(T * np.log(Y)).sum()
    return loss / T.shape[0] if normalize else loss


def mroc_auc_score(y_true, y_predictions):
    """ Returns a auc score. Handles multi-class

    For multi-class, the AUC score is in fact the MAUC
    score described in


    David J. Hand and Robert J. Till. 2001.
    A Simple Generalisation of the Area Under the ROC Curve
    for Multiple Class Classification Problems.
    Mach. Learn. 45, 2 (October 2001), 171-186.
    DOI=10.1023/A:1010920819831

    http://dx.doi.org/10.1023/A:1010920819831
    """
    (nb_rows, max_nb_classes) = y_predictions.shape
    # Today, it may happen that if a class appears only once in a dataset
    # it can appear in the train and not in the validation set.
    # In this case it will not be in y_true and
    # y_predictions.nb_cols is not exactly the number of class
    # to consider when computing the mroc_auc_score.
    classes = np.unique(y_true)
    nb_classes = len(classes)
    assert nb_classes <= max_nb_classes

    if nb_classes < 2:
        raise ValueError("Ended up with less than two-classes in the validation set.")

    if nb_classes == 2:
        return roc_auc_score(y_true, y_predictions[:, 1])

    def A(i, j):
        """
        Returns a asymmetric proximity metric, written A(i | j)
        in the paper.
        
        The sum of all (i, j) with  i != j
        will give us the symmetry.
        """
        mask = np.in1d(y_true, np.array([i, j]))
        y_true_i = y_true[mask] == i
        y_pred_i = y_predictions[mask][:, i]
        return roc_auc_score(y_true_i, y_pred_i)

    C = 1.0 / (nb_classes * (nb_classes - 1))
    return C * sum(
        A(i, j)
        for i in classes
        for j in classes
        if i != j)
