import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree

from . import helpers


def generate_decision_tree(
    data: list, feature_name: str, feature_label: str, target_name: str
):
    """
    Generates a regression decision tree based on the input data.

    Args:
        data (list): The input data containing features and target variable.
        feature_name (str): The name of the feature to be used for regression.
        feature_label (str): The label of the feature to be displayed in the decision tree plot.
        target_name (str): The name of the target variable.

    Returns:
        str: The ID of the saved figure.
    """

    # EXTRACT FEATURES AND TARGET VARIABLE FROM THE INPUT DATA
    features = np.array([[d[feature_name]] for d in data])
    target = np.array([d[target_name] for d in data])

    # SPLIT THE DATA INTO TRAINING AND TESTING SETS
    x_train, _x_test, y_train, _y_test = train_test_split(
        features, target, test_size=1, random_state=0
    )

    # CREATE A DECISION TREE REGRESSOR
    regressor = DecisionTreeRegressor(max_depth=3)

    # TRAIN THE REGRESSOR
    regressor.fit(x_train, y_train)

    # PLOT THE DECISION TREE
    plt.figure(figsize=(16, 10))
    plot_tree(
        regressor,
        filled=True,
        feature_names=[feature_label],
        impurity=False,
        rounded=True,
        proportion=True,
        # precision=0,
    )

    # SAVE THE FIGURE
    figure_id = helpers.generate_figure_id(feature_name, target_name)
    # plt.show()
    plt.savefig(f"./src/figures/{figure_id}.png", bbox_inches="tight")

    return figure_id


def generate_linear_regression(
    data: list,
    feature_name: str,
    feature_label: str,
    target_name: str,
    target_label: str,
    prediction_range: tuple,
):
    """
    Generates a linear regression graph based on the input data.

    Args:
        data (list): The input data containing features and target variable.
        feature_name (str): The name of the feature to be used for regression.
        feature_label (str): The label of the feature to be displayed in the linear regression plot.
        target_name (str): The name of the target variable.
        feature_label (str): The label of the target variable.

    Returns:
        str: The ID of the saved figure.
    """

    # EXTRACT FEATURES AND TARGET VARIABLE FROM THE INPUT DATA
    features = np.array([d[feature_name] for d in data]).reshape(-1, 1)
    target = np.array([d[target_name] for d in data])

    # CREATE A LINEAR REGRESSION MODEL
    model = LinearRegression()

    # FIT THE MODEL TO THE DATA
    model.fit(features, target)

    start, stop, step = prediction_range

    # MAKE PREDICTIONS ON NEW DATA POINTS
    new_features = np.array(
        [[prediction_val] for prediction_val in range(start, stop, step)]
    )
    prediction = model.predict(new_features)

    # PLOT THE ORIGINAL DATA POINTS AND THE LINEAR REGRESSION LINE
    plt.scatter(features, target, label="Original Data")
    plt.plot(new_features, prediction, "r-", label="Linear Regression Line")
    plt.xlabel(feature_label)
    plt.ylabel(target_label)
    plt.legend()

    # SAVE THE FIGURE
    figure_id = helpers.generate_figure_id(feature_name, target_name)
    # plt.show()
    plt.savefig(f"./src/figures/{figure_id}.png", bbox_inches="tight")

    return figure_id
