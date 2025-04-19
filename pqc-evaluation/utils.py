import argparse

def one_level(df_all, level, graphics):
    for graphic in graphics:
        if level != graphic['level']:
            df_all = df_all.drop([i for i in graphic['mechanisms']])
    return df_all

def split_mechanisms(input_mechanisms, mechanisms, normalize):
    """
    Matches user-specified mechanisms (KEM or signature) against available ones using name patterns.

    This function receives a list of mechanisms provided by the user, a list of available mechanisms
    (such as those returned by the OQS library), and a normalization dictionary that maps generic names
    (e.g., "falcon", "frodo-aes") to search patterns.

    The patterns can be:
    - A simple string (checks if it's contained in the mechanism name)
    - A tuple of strings (checks if all parts are contained in the mechanism name)

    Parameters:
        input_mechanisms (list[str]): List of mechanism names provided by the user.
        mechanisms (list[str]): List of all mechanisms available in the system.
        normalize (dict[str, str | tuple[str, ...]]): Mapping of generic names to search patterns.

    Returns:
        dict[str, list[str]]: A dictionary mapping each input mechanism to a list
                              of matching available mechanisms.

    Raises:
        argparse.ArgumentTypeError: If a mechanism is not recognized or no match is found.
    """
    matches = {}

    for mechanism in input_mechanisms:
        key = mechanism.lower()

        if key not in normalize:
            raise argparse.ArgumentTypeError(f"Unknown mechanism: {mechanism}")

        pattern = normalize[key]

        if isinstance(pattern, tuple):
            # Tupla with string patterns
            found = [
                alg for alg in mechanisms
                if all(p in alg.lower() for p in pattern)
            ]
        else:
            # A simple string pattern
            found = [
                alg for alg in mechanisms
                if pattern in alg.lower()
            ]

        if not found:
            raise argparse.ArgumentTypeError(f"No mechanism matched for: {mechanism}")

        matches[mechanism] = found

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