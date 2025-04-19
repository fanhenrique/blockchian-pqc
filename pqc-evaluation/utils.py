import argparse

def one_level(df_all, level, graphics):
    for graphic in graphics:
        if level != graphic['level']:
            df_all = df_all.drop([i for i in graphic['mechanisms']])
    return df_all

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