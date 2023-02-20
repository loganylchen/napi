# AUTOGENERATED! DO NOT EDIT! File to edit: ../005_metrics.ipynb.

# %% auto 0
__all__ = ['get_metrics', 'get_curves']

# %% ../005_metrics.ipynb 4
from sklearn.metrics import precision_recall_curve, \
    roc_curve, accuracy_score , f1_score, \
    precision_score, recall_score, confusion_matrix, auc


# %% ../005_metrics.ipynb 5
def get_metrics(y_true, y_pred):
    """Returns a dictionary of metrics for a given true and predicted set of labels.
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    metrics = {}
    metrics['accuracy'] = accuracy_score(y_true, y_pred)
    metrics['precision'] = precision_score(y_true, y_pred)
    metrics['recall'] = recall_score(y_true, y_pred)
    metrics['f1'] = f1_score(y_true, y_pred)
    metrics['specificity'] = tn / (tn + fp)
    metrics['fpr'] = fp / (fp + tn)
    return metrics

# %% ../005_metrics.ipynb 6
def get_curves(y_true, y_score):
    """Returns a dictionary of metrics for a given true and predicted set of labels.
    """
    precision, recall, pr_thresholds = precision_recall_curve(y_true, y_score)
    fpr, tpr, roc_thresholds = roc_curve(y_true, y_score)
    pr_auc = auc(recall, precision)
    roc_auc = auc(fpr, tpr)
    return {'precision': precision, 'recall': recall, 'pr_thresholds': pr_thresholds,
            'fpr': fpr, 'tpr': tpr, 'roc_thresholds': roc_thresholds,
            'pr_auc': pr_auc, 'roc_auc': roc_auc}