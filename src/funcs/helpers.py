import uuid
from datetime import datetime


def generate_figure_id(feature_name: str, target_name: str):
    """
    Generate a unique figure ID based on the feature name, target name, timestamp, and a unique UUID suffix.

    Args:
        feature_name (str): The name of the feature.
        target_name (str): The name of the target.

    Returns:
        str: The generated figure ID.
    """

    timestamp = int(datetime.now().timestamp())
    unique_suffix = uuid.uuid4().hex[:8]
    return f"{timestamp}-feature={feature_name}-target={target_name}-{unique_suffix}"
