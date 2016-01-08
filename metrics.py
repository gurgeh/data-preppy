from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
import matplotlib.pyplot as plt

from predict import get_XY


def metric(model, test_csv, fname):
    X, Y_true, headers = get_XY(test_csv)
    Y_pred = model.predict(X)
    try:
        print confusion_matrix(Y_true, [a[0] > 0.5 for a in Y_pred])
    except IndexError:
        print confusion_matrix(Y_true, [a > 0.5 for a in Y_pred])

    fpr, tpr, _ = roc_curve(Y_true, Y_pred)
    roc_auc = roc_auc_score(Y_true, Y_pred)

    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC - %s' % fname.split('/')[-1])
    plt.legend(loc="lower right")
    plt.show()
    plt.savefig(fname + ' - roc.png')
    return plt
