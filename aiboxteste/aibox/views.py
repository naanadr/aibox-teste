from django.shortcuts import render
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
import logging

from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import arff
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from aibox.forms import FileUploadForm


def plot_learning_curve(estimator, title, X, y, axes=None, ylim=None, cv=None,
                        n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):
    if axes is None:
        _, axes = plt.subplots(1, 3, figsize=(20, 5))

    axes[0].set_title(title)
    if ylim is not None:
        axes[0].set_ylim(*ylim)
    axes[0].set_xlabel("Training examples")
    axes[0].set_ylabel("Score")

    train_sizes, train_scores, test_scores, fit_times, _ = \
        learning_curve(estimator, X, y, cv=cv, n_jobs=n_jobs,
                       train_sizes=train_sizes,
                       return_times=True)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    fit_times_mean = np.mean(fit_times, axis=1)
    fit_times_std = np.std(fit_times, axis=1)

    # Plot learning curve
    axes[0].grid()
    axes[0].fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
    axes[0].fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1,
                         color="g")
    axes[0].plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
    axes[0].plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")
    axes[0].legend(loc="best")

    # Plot n_samples vs fit_times
    axes[1].grid()
    axes[1].plot(train_sizes, fit_times_mean, 'o-')
    axes[1].fill_between(train_sizes, fit_times_mean - fit_times_std,
                         fit_times_mean + fit_times_std, alpha=0.1)
    axes[1].set_xlabel("Training examples")
    axes[1].set_ylabel("fit_times")
    axes[1].set_title("Scalability of the model")

    # Plot fit_time vs score
    axes[2].grid()
    axes[2].plot(fit_times_mean, test_scores_mean, 'o-')
    axes[2].fill_between(fit_times_mean, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1)
    axes[2].set_xlabel("fit_times")
    axes[2].set_ylabel("Score")
    axes[2].set_title("Performance of the model")

    return plt


def read_data(data):
    X = []
    y = []

    for dat in data:
        new = []
        for i in range(len(dat)-1):
            new.append(dat[i])

        X.append(new)
        y.append(dat[len(dat)-1])

    return X, y


def train_model(classif, X, y, name, classif_name):
    models = {
        '1': SVC(gamma=0.001),
        '2': KNeighborsClassifier(n_neighbors=3),
        '3': LinearRegression()
    }

    fig, axes = plt.subplots(3, 1, figsize=(10, 15))
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)
    title = 'Learning Curves'
    plot_learning_curve(models[classif], title, X, y, axes=axes,
                        ylim=(0.7, 1.01), cv=cv, n_jobs=4)

    plt.savefig('aibox/static/plots/{}_{}.png'.format(name, classif_name),
                dpi=80)


def main_page(request):
    context = {}

    if request.method == 'GET':
        form = FileUploadForm()
        context['form'] = form
    else:
        try:
            form = FileUploadForm(request.POST, request.FILES)
            classif = form.data.get('classificador')

            models = {
                '1': 'svc',
                '2': 'knn',
                '3': 'linear'
            }

            arquivo = request.FILES['arquivo']
            name = arquivo.name.split('.arff')[0]

            content = arquivo.read().decode('utf-8')
            f = StringIO(content)
            data, meta = arff.loadarff(f)

            X, y = read_data(data)

            train_model(classif, X, y, name, models[classif])

            if form.is_valid():
                form.save()

            context['plot'] = 'plots/{}_{}.png'.format(name, models[classif])
            context['form'] = form

            messages.success(request, 'Modelo treinado com sucesso, '
                             'obrigado por aguardar!')
        except Exception as e:
            messages.warning(request, 'Não foi possível fazer upload!')
            logging.getLogger('error_logger').error('Nao foi possivel fazer '
                                                    'upload do arquivo. '
                                                    '{}'.format(repr(e)))

    return render(request, 'aibox/main_page.html', context)
