import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

from . import helpers


def generate_decision_tree(
    data: list, feature_name: str, feature_label: str, target_name: str
):
    """
    Generates a classification decision tree based on the input data.

    Args:
        data (list): The input data containing features and target variable.
        feature_name (str): The name of the feature to be used for classification.
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
    classifier = DecisionTreeClassifier(max_depth=3)

    # TRAIN THE REGRESSOR
    classifier.fit(x_train, y_train)

    # PLOT THE DECISION TREE
    plt.figure(figsize=(16, 10))
    plot_tree(
        classifier,
        filled=True,
        feature_names=[feature_label],
        rounded=True,
    )

    # SAVE THE FIGURE
    figure_id = helpers.generate_figure_id(feature_name, target_name)
    # plt.show()
    plt.savefig(f"./src/figures/{figure_id}.png", bbox_inches="tight")

    return figure_id
