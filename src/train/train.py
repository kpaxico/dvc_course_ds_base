import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import f1_score, make_scorer
from typing import Dict, Text
import numpy as np
import random


class UnsupportedClassifier(Exception):

    def __init__(self, estimator_name):

        self.msg = f"Unsupported estimator {estimator_name}"
        super().__init__(self.msg)


def get_supported_estimator() -> Dict:
    """
    Returns:
        Dict: supported classifiers
    """

    return {"logreg": LogisticRegression, "svm": SVC, "knn": KNeighborsClassifier}


def train(
    df: pd.DataFrame,
    target_column: Text,
    estimator_name: Text,
    param_grid: Dict,
    cv: int,
    random_seed: int = 42,
):
    """Train model.
    Args:
        df {pandas.DataFrame}: dataset
        target_column {Text}: target column name
        estimator_name {Text}: estimator name
        param_grid {Dict}: grid parameters
        cv {int}: cross-validation value
        random_seed {int}: random seed for reproducibility
    Returns:
        trained model
    """

    np.random.seed(random_seed)
    random.seed(random_seed)

    estimators = get_supported_estimator()

    if estimator_name not in estimators.keys():
        raise UnsupportedClassifier(estimator_name)

    # Pass random_state if supported
    estimator_class = estimators[estimator_name]
    estimator_args = {}
    if "random_state" in estimator_class().get_params():
        estimator_args["random_state"] = random_seed
    estimator = estimator_class(**estimator_args)
    f1_scorer = make_scorer(f1_score, average="weighted")
    clf = GridSearchCV(
        estimator=estimator, param_grid=param_grid, cv=cv, verbose=1, scoring=f1_scorer
    )
    # Get X and Y
    y_train = df.loc[:, target_column].values.astype("int32")
    X_train = df.drop(target_column, axis=1).values.astype("float32")
    clf.fit(X_train, y_train)

    return clf
