import random
import uuid


def generate_labels_mapping(labels, has_colors=True):
    """
    Generate a mapping of labels with unique IDs, names, and random colors.

    Args:
        labels (list): A list of labels.
        has_colors (bool): Flag indicating whether to include colors in the mapping.

    Returns:
        dict: A dictionary containing the labels mapping with unique IDs, names, and colors (if has_colors is True).
    """
    labels_mapping = []
    for label in labels:
        label_mapping = {
            "id": str(uuid.uuid4()),
            "label": label,
        }
        if has_colors:
            label_mapping["color"] = "#%06x" % random.randint(0, 0xFFFFFF)
        labels_mapping.append(label_mapping)

    return {"labels": labels_mapping}
