from datetime import datetime
import pandas as pd
import oqs
import argparse
import os

# internal imports
import utils
import kem
import sig

DIR_RESULTS = 'results'


KEM_MECHANISMS =  {
    'bike': {
        'include': ['bike'],
    },
    'hqc': {
        'include': ['hqc'],
    },
    'kyber': {
        'include': ['kyber'],
    },
     'sntrup': {
        'include': ['sntrup'],
    },
    'mceliece': {
        'include': ['classic-mceliece'],
    },
    'mlkem': {
        'include': ['ml-kem'],
    },
    'frodo-aes': {
        'include': ['frodokem', 'aes'],
    },
    'frodo-shake': {
        'include': ['frodokem', 'shake'],
    },
}


SIG_MECHANISMS = {
    "falcon": {
        "include": ["falcon"],
        "exclude": ["padded"]
    },
    "falcon-padded": {
        "include": ["falcon", "padded"]
    },
    "dilithium": {
        "include": ["dilithium"]
    },
    "mldsa": {
        "include": ["ml-dsa"]
    },
    "sphincs-sha": {
        "include": ["sphincs", "sha2"]
    },
    "sphincs-shake": {
        "include": ["sphincs", "shake"]
    }
}


def load_mechanisms(input_mechanisms, oqs_get_mechanisms, normalize):

    oqs_mechanisms = oqs_get_mechanisms()
    mechanisms = utils.split_mechanisms(input_mechanisms=input_mechanisms, mechanisms=oqs_mechanisms, normalize=normalize)
    
    return mechanisms


def save_results(df, mechanisms, number=None):

    os.makedirs(DIR_RESULTS, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    mechanisms_str = '_'.join(mechanisms)

    if number:
        file = f'{DIR_RESULTS}/{timestamp}_times-{number}x_{mechanisms_str}.csv'    
    else:
        file = f'{DIR_RESULTS}/{timestamp}_sizes_{mechanisms_str}.csv'

    df.to_csv(file, index=False)
    
    print(f'File {file} was created')


def run_times(mechanisms, times_evaluation, number):

    results_times = []
    for mechanism, variants in mechanisms.items():
        for variant in variants:
            results_times.append(times_evaluation(variant, number))

    return pd.concat(results_times)

def run_sizes(mechanisms, sizes_evaluation):

    results_sizes = []
    for mechanism, variants in mechanisms.items():
        for variant in variants:
           results_sizes.append(sizes_evaluation(variant))

    return pd.DataFrame(results_sizes)


def print_variants(mechanisms, oqs_mechanisms, normalize):

    mechanism_groups = load_mechanisms(
        input_mechanisms=mechanisms.keys(),
        oqs_get_mechanisms=oqs_mechanisms,
        normalize=normalize
    )

    for mechanism, variants in mechanism_groups.items():
        print(f"{mechanism}:")
        for variant in variants:
            print(f"  - {variant}")

def main():

    parser = argparse.ArgumentParser(
        description="PQC Evaluation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--kem', help='List KEM algorithms', type=str, nargs='+', choices=list(KEM_MECHANISMS.keys()))
    parser.add_argument('--sig', help='List signature algorithms', type=str, nargs='+', choices=list(SIG_MECHANISMS.keys()))
    # TODO ainda não funciona, vai implementar
    parser.add_argument("--list_kem", help="List of variants KEM algorithms", action="store_true")
    parser.add_argument("--list_sig", help="List of variants digital signature algorithms", action="store_true")
    
    args = parser.parse_args()

    print(args)

    if args.list_kem:
        print("List of KEM algorithm variants")
        print(oqs.get_enabled_kem_mechanisms())
        # print(oqs.get_supported_kem_mechanisms())

        print_variants(
            mechanisms=KEM_MECHANISMS,
            oqs_mechanisms=oqs.get_enabled_kem_mechanisms,
            normalize=KEM_MECHANISMS
        )

    if args.list_sig:
        print("Digital Signature ")
        print(oqs.get_enabled_sig_mechanisms())
        # print(oqs.get_supported_sig_mechanisms())

        print_variants(
            mechanisms=SIG_MECHANISMS,
            oqs_mechanisms=oqs.get_enabled_sig_mechanisms,
            normalize=SIG_MECHANISMS
        )

    if args.kem:

        kem_mechanisms = load_mechanisms(input_mechanisms=args.kem, oqs_get_mechanisms=oqs.get_enabled_kem_mechanisms, normalize=KEM_MECHANISMS)

        print(kem_mechanisms)

        # KEM times
        df_kem_times = run_times(kem_mechanisms, kem.times_evaluation, args.number)
        save_results(df=df_kem_times,  mechanisms=args.kem, number=args.number)
        
        # KEM sizes
        df_kem_sizes = run_sizes(kem_mechanisms, kem.sizes_evaluation)
        save_results(df=df_kem_sizes, mechanisms=args.kem)

    if args.sig:

        sig_mechanisms = load_mechanisms(input_mechanisms=args.sig, oqs_get_mechanisms=oqs.get_enabled_sig_mechanisms, normalize=SIG_MECHANISMS)

        print(sig_mechanisms)

        # Signature times
        df_sig_times = run_times(sig_mechanisms, sig.times_evaluation, args.number)
        save_results(df=df_sig_times, mechanisms=args.sig, number=args.number)

        # Signature sizes
        df_sig_sizes = run_sizes(sig_mechanisms, sig.sizes_evaluation)
        save_results(df=df_sig_sizes,  mechanisms=args.sig)

if __name__ == '__main__':
    main()