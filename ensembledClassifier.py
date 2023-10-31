import sklearn
import torch
import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

lrCLF = LogisticRegression(random_state=0)
svmCLF = svm.SVC()
nbCLF = GaussianNB()
rfCLF = RandomForestClassifier(n_estimators=20)

models = [lrCLF, svmCLF, nbCLF, rfCLF]

df = pd.read_csv('annotated_predicted_triples.csv')

for i in list(range(len(models))):
    labeled_df = df[df['labeled_class'] != -1]
    unlabeled_df = df[df['labeled_class'] == -1]

    x_labeled = labeled_df[['triple_name', 'score', 'triple_incidence', 'head_rate', 'tail_rate']]
    y_labeled = labeled_df['labeled_class']

    x_train, x_test, y_train, y_test = train_test_split(x_labeled, y_labeled, test_size=0.1, random_state=0)

    x_unlabeled = unlabeled_df[['triple_name', 'score', 'triple_incidence', 'head_rate', 'tail_rate']]

    # initial training'
    regressor = models[i]

    regressor.fit(x_train[['score', 'triple_incidence', 'head_rate', 'tail_rate']], y_train)

    modelName = ""
    if(i == 0):
        modelName = "logisticRegression"
    elif(i == 1):
        modelName = "supportVectorMachine"
    elif(i == 2):
        modelName = "naiveBayesClassifier"
    elif(i == 3):
        modelName = "randomForestClassifier"

    # self-training loop
    for iteration in range(100):
        # predict unlabeled data
        prediction = regressor.predict(x_unlabeled[['score', 'triple_incidence', 'head_rate', 'tail_rate']])
        # test on labeled data
        # y_pred_test = regressor.predict(x_test[['score', 'triple_incidence', 'head_rate', 'tail_rate']])
        # print(f'iteration {iteration}')
        # print(classification_report(y_test, y_pred_test))
        # get the most confident predictions
        indices = np.argsort(prediction)[-2:]
        # add them to labeled data
        x_train = pd.concat([x_train, x_unlabeled.iloc[indices]])
        y_train = pd.concat([y_train, pd.Series(prediction[indices])])
        # remove them from unlabeled data
        x_unlabeled = x_unlabeled.drop(x_unlabeled.index[indices])
        # train again
        regressor.fit(x_train[['score', 'triple_incidence', 'head_rate', 'tail_rate']], y_train)

    # Final prediction and evaluation on the test data
    y_pred_test = regressor.predict(x_test[['score', 'triple_incidence', 'head_rate', 'tail_rate']])
    print(classification_report(y_test, y_pred_test))

    # Final prediction on the entire data and save to file
    prediction = regressor.predict(x_unlabeled[['score', 'triple_incidence', 'head_rate', 'tail_rate']])
    x = pd.concat([x_test, x_train, x_unlabeled])
    y = pd.concat([y_test, y_train, pd.Series(prediction)])
    x['predicted_class'] = y.values
    x.to_csv(f'combined_data_class_x_n_est_{modelName}.csv', index=False)

    df['predicted_class'] = regressor.predict(df[['score', 'triple_incidence', 'head_rate', 'tail_rate']])
    # count the number of 1s
    print(df['predicted_class'].value_counts())
    df.to_csv(f'combined_predicted_classification_n_est_{modelName}.csv', index=False)