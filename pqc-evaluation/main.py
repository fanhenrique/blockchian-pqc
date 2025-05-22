from datetime import datetime
import pandas as pd
import oqs
import argparse
import os

# internal imports
import utils
import kem
import sig
from rules import KEM_MECHANISMS, SIG_MECHANISMS

DIR_RESULTS = "results"

def loads_mechanisms(input_mechanisms, oqs_get_mechanisms, normalizer, oqs_cls):

    oqs_mechanisms = oqs_get_mechanisms()

    mechanisms = utils.mechanisms_groups(
        input_mechanisms=input_mechanisms,
        mechanisms=oqs_mechanisms,
        normalizer=normalizer,
        oqs_cls=oqs_cls
    )
    
    return mechanisms


def save_results(df, mechanisms, number=None):

    os.makedirs(DIR_RESULTS, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    mechanisms_str = "_".join(mechanisms)

    if number:
        file = f"{DIR_RESULTS}/{timestamp}_time-evaluation-{number}x_{mechanisms_str}.csv"
    else:
        file = f"{DIR_RESULTS}/{timestamp}_size-evaluation_{mechanisms_str}.csv"

    df.to_csv(file, index=False)
    
    print(f"File {file} was created")


def run_times(mechanisms, times_evaluation, number):

    results_times = []
    for mechanism, variants in mechanisms.items():
        for variant in variants.values():
            results_times.append(times_evaluation(variant, number))

    return pd.concat(results_times)

def run_sizes(mechanisms, sizes_evaluation):

    results_sizes = []
    for mechanism, variants in mechanisms.items():
        for variant in variants.values():
           results_sizes.append(sizes_evaluation(variant))

    return pd.DataFrame(results_sizes)


def print_variants(mechanisms, oqs_mechanisms, normalizer, oqs_cls):

    mechanism_groups = loads_mechanisms(
        input_mechanisms=mechanisms.keys(),
        oqs_get_mechanisms=oqs_mechanisms,
        normalizer=normalizer,
        oqs_cls=oqs_cls
    )
            
    print(mechanism_groups)
    for mechanism, variants in mechanism_groups.items():
        print(f"{mechanism}:")
        for level, variant in variants.items():
            print(f"{4 * ' '}{variant} - NIST Level {level}")
            

def evaluation(mechanisms, oqs_mechanisms, oqs_cls, normalizer, time_evaluation, size_evaluation, number_executions):

    mechanisms_groups = loads_mechanisms(
        input_mechanisms=mechanisms,
        oqs_get_mechanisms=oqs_mechanisms,
        normalizer=normalizer,
        oqs_cls=oqs_cls
    )

    # time evaluation
    df_time_evaluation = run_times(mechanisms_groups, time_evaluation, number_executions)
    save_results(df=df_time_evaluation, mechanisms=mechanisms, number=number_executions)

    # size evaluation
    df_size_evaluation = run_sizes(mechanisms_groups, size_evaluation)
    save_results(df=df_size_evaluation, mechanisms=mechanisms)


def main():

    parser = argparse.ArgumentParser(
        description="PQC Evaluation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--kem", help="Input list of KEM algorithms", type=str, nargs="+", choices=list(KEM_MECHANISMS.keys()))
    parser.add_argument("--sig", help="Input list of digital signature algorithms", type=str, nargs="+", choices=list(SIG_MECHANISMS.keys()))
    # TODO ainda não funciona, vai implementar
    # parser.add_argument("--levels", "-l", help="Nist level", type=int, choices=range(1, 6), nargs="+")
    parser.add_argument("--number", "-n", help="Number of executions", type=utils.positive_int, default=1)
    parser.add_argument("--list-kem", help="List of variants KEM algorithms", action="store_true")
    parser.add_argument("--list-sig", help="List of variants digital signature algorithms", action="store_true")
    
    args = parser.parse_args()

    # print(args)

    if args.list_kem:
        print("List of KEM algorithm variants")
        # print(oqs.get_enabled_kem_mechanisms())
        # print(oqs.get_supported_kem_mechanisms())

        print_variants(
            mechanisms=KEM_MECHANISMS,
            oqs_mechanisms=oqs.get_enabled_kem_mechanisms,
            normalizer=KEM_MECHANISMS,
            oqs_cls=oqs.KeyEncapsulation
        )

    if args.list_sig:
        print("Digital Signature ")
        # print(oqs.get_enabled_sig_mechanisms())
        # print(oqs.get_supported_sig_mechanisms())

        print_variants(
            mechanisms=SIG_MECHANISMS,
            oqs_mechanisms=oqs.get_enabled_sig_mechanisms,
            normalizer=SIG_MECHANISMS,
            oqs_cls=oqs.Signature
        )

    if args.kem:
        evaluation(
            mechanisms=args.kem,
            oqs_mechanisms=oqs.get_enabled_kem_mechanisms,
            oqs_cls=oqs.KeyEncapsulation,
            normalizer=KEM_MECHANISMS,
            time_evaluation=kem.time_evaluation,
            size_evaluation=kem.size_evaluation,
            number_executions=args.number
        )

    if args.sig:
        evaluation(
            mechanisms=args.sig,
            oqs_mechanisms=oqs.get_enabled_sig_mechanisms,
            oqs_cls=oqs.Signature,
            normalizer=SIG_MECHANISMS,
            time_evaluation=sig.time_evaluation,
            size_evaluation=sig.size_evaluation,
            number_executions=args.number
        )

if __name__ == "__main__":
    main()