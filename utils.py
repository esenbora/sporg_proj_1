import numpy as np
import pandas as pd
from thefuzz import process, fuzz


def find_best_match(input_string, choices_dict, threshold=80):
    """
    AI-GENERATED (GLM 4.6)
    Finds the best match for an input string in a dictionary's keys
    and returns the corresponding value.

    Args:
        input_string (str): The string to find a match for.
        choices_dict (dict): The dictionary with canonical keys.
        threshold (int): The minimum similarity score (0-100) to accept a match.

    Returns:
        The value from the dictionary if a good match is found, otherwise np.nan.
    """
    # process.extractOne returns a tuple: (best_match, score)
    best_match, score = process.extractOne(
        input_string,
        choices=choices_dict.keys(),
        scorer=fuzz.WRatio # WRatio is good for handling different cases and lengths
    )

    # If the score is above our threshold, return the value
    if score >= threshold:
        return choices_dict[best_match]
    else:
        # Return a default value (e.g., NaN) if no good match is found
        return np.nan