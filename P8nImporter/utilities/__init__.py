def generate_random_id():
    """
    Generate a random id.

    Returns:
        str: The random id.
    """
    import random
    import string

    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
