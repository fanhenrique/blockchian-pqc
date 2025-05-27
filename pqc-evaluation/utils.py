import argparse
import oqs

def one_level(df_all, level, graphics):
    for graphic in graphics:
        if level != graphic['level']:
            df_all = df_all.drop([i for i in graphic['mechanisms']])
    return df_all


def get_variants_by_level(df, variant_dict):
    csv_variants = set(df.index.to_list())

    variants_by_level = {}

    for scheme, levels in variant_dict.items():
        for level, variant_name in levels.items():
            if variant_name in csv_variants:
                variants_by_level.setdefault(level, []).append(variant_name)

    return dict(sorted(variants_by_level.items()))

def mechanisms_groups(input_mechanisms, mechanisms, normalizer, nist_levels, oqs_cls):
    """
    Filters and groups cryptographic mechanisms based on inclusion/exclusion patterns 
    and maps them to their respective NIST security levels.

    For each mechanism in `input_mechanisms`, the function applies normalization rules 
    defined in the `normalizer` to filter matching mechanisms from the `mechanisms` list.
    The filtered mechanisms are then classified by their claimed NIST security level 
    using the `oqs_cls` interface.

    Args:
        input_mechanisms (list of str): 
            List of mechanism identifiers to be normalized and grouped.
        
        mechanisms (list of str): 
            Complete list of available mechanisms to be filtered.
        
        normalizer (dict): 
            A dictionary defining filtering rules for each mechanism. 
            Each key corresponds to an input mechanism name, and its value is 
            a dictionary with the keys:
                - "include": list or string of substrings that must be present.
                - "exclude": list or string of substrings that must NOT be present.
        
        oqs_cls (class): 
            Callable class that initializes a mechanism instance exposing a 
            `details` attribute containing the 'claimed_nist_level' key.

    Returns:
        dict: 
            Dictionary mapping each input mechanism to its matched variants 
            organized by NIST security level. Example structure:

            mechanism_groups: {
                mechanism_1: {
                    {level_1: variant_1}, 
                    ...,
                    {level_5: variant_5}, 
                },
                ...,
                mechanism_N: {
                    {level_1: variant_1}, 
                    ...,
                    {level_5: variant_5}, 
                }
            }
    
    Raises:
        argparse.ArgumentTypeError: 
            - If an input mechanism is not defined in the `normalizer`.
            - If no matching mechanisms are found for an input mechanism.

        ValueError:
            If a matched mechanism does not provide a 'claimed_nist_level' 
            in its details.    
    """

    matches = {}
    
    for input_mechanism in input_mechanisms:
        
        if input_mechanism not in normalizer:
            raise argparse.ArgumentTypeError(f"Unknown mechanism: {input_mechanism}")

        rule = normalizer[input_mechanism]
        include = rule.get("include", [])
        exclude = rule.get("exclude", [])

        include = [include] if isinstance(include, str) else include
        exclude = [exclude] if isinstance(exclude, str) else exclude

        founds = []

        for mechanism in mechanisms:
            mechanism_lower = mechanism.lower()

            if all(p in mechanism_lower for p in include):
                if any(p in mechanism_lower for p in exclude):
                    continue
                founds.append(mechanism)

        # if not founds:
            # raise argparse.ArgumentTypeError(f"No mechanism matched for: {input_mechanism}")
        
        variants_with_levels = {}
        for variant in founds:
            with oqs_cls(variant) as oqs_variant:
                level = oqs_variant.details.get('claimed_nist_level', None)
                if level is None:
                    raise ValueError(f"NIST level not found for {variant}")
                if level in nist_levels:
                    variants_with_levels[level] = variant
                    
        if variants_with_levels:
            matches[input_mechanism] = variants_with_levels

    return matches


def get_ecdsa_mechanisms(input_mechanisms, curves, nist_levels):
    
    matches = {}
    
    for mechanism in input_mechanisms:
        if mechanism == "ecdsa":
            variants_with_levels = {}
            for level, variant in curves.items():

                if level in nist_levels:
                    variants_with_levels[level] = variant
        
            if variants_with_levels: 
                matches[mechanism] = variants_with_levels         
        
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