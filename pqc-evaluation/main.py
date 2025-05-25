from datetime import datetime
import pandas as pd
import oqs
import argparse
import os

# internal imports
import utils
import kem
import sig
import ecdsa
from rules import KEM_MECHANISMS, SIG_MECHANISMS, CURVES

DIR_RESULTS = "results"

def save_results(dfs, input_mechanisms):

    os.makedirs(DIR_RESULTS, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    mechanisms_str = "_".join(input_mechanisms)

    for key, df in dfs.items():
        file = f"{DIR_RESULTS}/{timestamp}_{key}_{mechanisms_str}.csv"
        save_csv(df, file)

def save_csv(df, file):
    df.to_csv(file, index=False)
    print(f"File {file} was created")


def run_times(mechanisms, oqs_time_evaluation, number, ecdsa_time_evaluation=None):

    results_times = []
    for mechanism, variants in mechanisms.items():
        if mechanism == "ecdsa":
            for variant in variants.values():
                results_times.append(ecdsa_time_evaluation(variant, number))
        else:
            for variant in variants.values():
                results_times.append(oqs_time_evaluation(variant, number))

    return pd.concat(results_times)

def run_sizes(mechanisms, sizes_evaluation):

    results_sizes = []
    for mechanism, variants in mechanisms.items():
        for variant in variants.values():
           results_sizes.append(sizes_evaluation(variant))

    return pd.DataFrame(results_sizes)


def print_variants(input_mechanisms, oqs_mechanisms, normalizer, nist_levels, oqs_cls, ecds_mechanisms=None):

    oqs_mechanisms_groups = utils.mechanisms_groups(
        input_mechanisms=input_mechanisms,
        mechanisms=oqs_mechanisms(),
        normalizer=normalizer,
        nist_levels=nist_levels,
        oqs_cls=oqs_cls
    )

    for mechanism, variants in mechanism_groups.items():
        print(f"{mechanism}:")
        for level, variant in variants.items():
            print(f"{4 * ' '}{variant} - NIST Level {level}")


def compute_mean_std(df, group_by, columns):
    """
    Compute mean and standard deviation for specified columns grouped by a key.

    Parameters:
    - df: The input DataFrame.
    - group_by: Column name to group by (e.g., 'variant').
    - columns: List of column names to compute mean and std for.

    Returns:
    - pd.DataFrame: DataFrame with mean and std columns.
    """
    grouped = df.groupby(group_by)

    result = pd.DataFrame()
    for col in columns:
        result[f'mean_{col}'] = grouped[col].mean()
        result[f'std_{col}'] = grouped[col].std()

    # Transform the index into a column
    result = result.reset_index()
    return result


def kem_evaluation(
    input_mechanisms,
    oqs_mechanisms,
    normalizer,
    nist_levels,
    oqs_cls,
    number_executions,
    size_evaluation=None,
    oqs_time_evaluation=None
):

    oqs_mechanisms = oqs_mechanisms()

    oqs_mechanisms_groups = utils.mechanisms_groups(
        input_mechanisms=input_mechanisms,
        mechanisms=oqs_mechanisms,
        normalizer=normalizer,
        nist_levels=nist_levels,
        oqs_cls=oqs_cls
    )

    # time evaluation
    df_time_evaluation = run_times(oqs_mechanisms_groups, oqs_time_evaluation, number_executions)

    # Compute mean and std of time evaluation
    df_time_evaluation_mean_std = compute_mean_std(
        df=df_time_evaluation,
        group_by='variant',
        columns=["keypair", "encrypt", "decrypt"]
    )

    # size evaluation
    df_size_evaluation = run_sizes(oqs_mechanisms_groups, size_evaluation)

    dfs = {
        f"time-evaluation-{number_executions}x": df_time_evaluation,
        "size-evaluation": df_size_evaluation,
    }

    save_results(dfs=dfs, input_mechanisms=input_mechanisms)


def sig_evaluation(
    input_mechanisms,
    oqs_mechanisms,
    normalizer,
    nist_levels,
    oqs_cls,
    number_executions,
    size_evaluation=None,
    oqs_time_evaluation=None,
    ecdsa_time_evaluation=None,
):

    oqs_mechanisms = oqs_mechanisms()

    oqs_mechanisms_groups = utils.mechanisms_groups(
        input_mechanisms=input_mechanisms,
        mechanisms=oqs_mechanisms,
        normalizer=normalizer,
        nist_levels=nist_levels,
        oqs_cls=oqs_cls
    )

    if 'ecdsa' in input_mechanisms:
        ecdsa_mechanisms_groups = utils.get_ecdsa_mechanisms(
            input_mechanisms= input_mechanisms,
            curves=CURVES,
            nist_levels=nist_levels
        )

    combined = {}
    for mechanism in input_mechanisms:
        if mechanism in oqs_mechanisms_groups:
            combined[mechanism] = oqs_mechanisms_groups[mechanism]
        elif mechanism in ecdsa_mechanisms_groups:
            combined[mechanism] = ecdsa_mechanisms_groups[mechanism]
        else:
            raise ValueError(f"Mechanism '{mech}' not found in oqs_mechanisms_groups or ecdsa_mechanisms_groups")
    
    # time evaluation
    df_time_evaluation = run_times(
        mechanisms=combine_mechanism_groups,
        oqs_time_evaluation=oqs_time_evaluation,
        ecdsa_time_evaluation=ecdsa_time_evaluation,
        number=number_executions
    )

    # Compute mean and std of time evaluation
    df_time_evaluation_mean_std = compute_mean_std(
        df=df_time_evaluation,
        group_by='variant',
        columns=["keypair", "sign", "verify"]
    )
    
    # size evaluation
    df_size_evaluation = run_sizes(oqs_mechanisms_groups, size_evaluation)

    dfs = {
        f"time-evaluation-{number_executions}x": df_time_evaluation,
        "time-evaluation-mean-std": df_time_evaluation_mean_std,
        "size-evaluation": df_size_evaluation,
    }

    save_results(dfs=dfs, input_mechanisms=input_mechanisms)

def main():

    parser = argparse.ArgumentParser(
        description="PQC Evaluation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--kem", help="Input list of KEM algorithms", type=str, nargs="+", choices=list(KEM_MECHANISMS.keys()))
    parser.add_argument("--sig", help="Input list of digital signature algorithms", type=str, nargs="+", choices=list(SIG_MECHANISMS.keys()))
    parser.add_argument("--levels", "-l", help="Nist levels", type=int, choices=range(1, 6), default=(range(1,6)), nargs="+")
    parser.add_argument("--number", "-n", help="Number of executions", type=utils.positive_int, default=1)
    parser.add_argument("--list-kem", help="List of variants KEM algorithms", action="store_true")
    parser.add_argument("--list-sig", help="List of variants digital signature algorithms", action="store_true")
    
    args = parser.parse_args()

    if args.list_kem:
        print("List of KEM algorithm variants")
        # print(oqs.get_enabled_kem_mechanisms())
        # print(oqs.get_supported_kem_mechanisms())

        print_variants(
            input_mechanisms=KEM_MECHANISMS.keys(),
            oqs_mechanisms=oqs.get_enabled_kem_mechanisms,
            normalizer=KEM_MECHANISMS,
            nist_levels=args.levels,
            oqs_cls=oqs.KeyEncapsulation
        )

    if args.list_sig:
        print("Digital Signature ")
        # print(oqs.get_enabled_sig_mechanisms())
        # print(oqs.get_supported_sig_mechanisms())

        print_variants(
            input_mechanisms=SIG_MECHANISMS.keys(),
            oqs_mechanisms=oqs.get_enabled_sig_mechanisms,
            normalizer=SIG_MECHANISMS,
            nist_levels=args.levels,
            oqs_cls=oqs.Signature
        )

    if args.kem:
        kem_evaluation(
            input_mechanisms=args.kem,
            oqs_mechanisms=oqs.get_enabled_kem_mechanisms,
            normalizer=KEM_MECHANISMS,
            nist_levels=args.levels,
            oqs_cls=oqs.KeyEncapsulation,      
            oqs_time_evaluation=kem.time_evaluation,
            number_executions=args.number,
            size_evaluation=kem.size_evaluation,
        )

    if args.sig:
        sig_evaluation(
            input_mechanisms=args.sig,
            oqs_mechanisms=oqs.get_enabled_sig_mechanisms,
            normalizer=SIG_MECHANISMS,
            nist_levels=args.levels,
            oqs_cls=oqs.Signature,
            oqs_time_evaluation=sig.time_evaluation,
            ecdsa_time_evaluation=ecdsa.time_evaluation,
            number_executions=args.number,
            size_evaluation=sig.size_evaluation,
        )

if __name__ == "__main__":
    main()