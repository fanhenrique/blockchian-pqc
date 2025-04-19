import argparse

def one_level(df_all, level, graphics):
    for graphic in graphics:
        if level != graphic['level']:
            df_all = df_all.drop([i for i in graphic['mechanisms']])
    return df_all

def split_mechanisms(input_mechanisms, mechanisms, normalize):
    """
    Filters and groups mechanisms based on inclusion and exclusion rules.

    For each mechanism in `input_mechanisms`, applies normalization rules from
    the `normalize` dictionary to identify matching mechanisms in the `mechanisms` list.
    Each rule may include patterns to include and/or exclude.

    Args:
        input_mechanisms (list of str): List of mechanism names to normalize and match.
        mechanisms (list of str): Full list of available mechanisms to filter.
        normalize (dict): Dictionary where keys are mechanism names and values are
            rules containing "include" and "exclude" keys that define filtering patterns.

    Returns:
        dict: A dictionary where each key is an item from `input_mechanisms`, and each value
            is a list of mechanisms from `mechanisms` that match the inclusion/exclusion rules.

    Raises:
        argparse.ArgumentTypeError: If a mechanism is not defined in `normalize` or if no
            matching mechanisms are found for a given input.
    """

    matches = {}
    
    for input_mechanism in input_mechanisms:
        
        if input_mechanism not in normalize:
            raise argparse.ArgumentTypeError(f"Unknown mechanism: {input_mechanism}")

        rule = normalize[input_mechanism]
        include = rule.get("include", [])
        exclude = rule.get("exclude", [])

        # Ensure include/exclude are lists
        if isinstance(include, str):
            include = [include]
        if isinstance(exclude, str):
            exclude = [exclude]

        founds = []

        for mechanism in mechanisms:
            mech_lower = mechanism.lower()
            
            # Check if all include patterns are present
            if all(p in mech_lower for p in include):
            
                # Skip if any exclude pattern is present
                if any(p in mech_lower for p in exclude):
                    continue
                founds.append(mechanism)

        if not founds:
            raise argparse.ArgumentTypeError(f"No mechanism matched for: {input_mechanism}")
        
        matches[input_mechanism] = founds

    return matches

def positive_int(value: int):
    """
    Validates that the provided value is a positive integer.

    Parameters:
        value (int): The value to validate.

    Returns:
        int: The validated positive integer.

    Raises:
        argparse.ArgumentTypeError: If the value is not a positive integer.
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue