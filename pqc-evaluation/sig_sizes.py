# Signature Python example

import pandas as pd
import matplotlib.pyplot as plt

import oqs
from pprint import pprint

# print("liboqs version:", oqs.oqs_version())
# print("liboqs-python version:", oqs.oqs_python_version())
# print("Enabled signature mechanisms:")
# sigs = oqs.get_enabled_sig_mechanisms()
# pprint(sigs, compact=True)

message = "This is the message to sign".encode()

# Create signer and verifier with sample signature mechanisms
# sigalg = "Dilithium2"


list_df = []

for sigalg in oqs.get_enabled_sig_mechanisms():

    sig_mechanism = []
    is_euf_cma = []
    claimed_nist_level = []
    length_public_key = []
    length_secret_key = []
    length_signature = []


    df = pd.DataFrame({
        'sig_mechanism': [], 
        'is_euf_cma': [], 
        'claimed_nist_level': [], 
        'length_public_key': [],
        'length_secret_key': [],
        'length_signature': []
    })

    with oqs.Signature(sigalg) as signer:
        with oqs.Signature(sigalg) as verifier:
            # print("\nSignature details:")
            # pprint(signer.details)

            sig_mechanism.append(sigalg)
            is_euf_cma.append(signer.details['is_euf_cma'])
            claimed_nist_level.append(signer.details['claimed_nist_level'])
            length_public_key.append(signer.details['length_public_key'])
            length_secret_key.append(signer.details['length_secret_key'])
            length_signature.append(signer.details['length_signature'])

            # Signer generates its keypair
            signer_public_key = signer.generate_keypair()
            # Optionally, the secret key can be obtained by calling export_secret_key()
            # and the signer can later be re-instantiated with the key pair:
            # secret_key = signer.export_secret_key()

            # Store key pair, wait... (session resumption):
            # signer = oqs.Signature(sigalg, secret_key)

            # Signer signs the message
            signature = signer.sign(message)

            # Verifier verifies the signature
            is_valid = verifier.verify(message, signature, signer_public_key)

            # print("\nValid signature?", is_valid)

    df['sig_mechanism'] = pd.Series(sig_mechanism)
    df['is_euf_cma'] = pd.Series(is_euf_cma)
    df['claimed_nist_level'] = pd.Series(claimed_nist_level)
    df['length_public_key'] = pd.Series(length_public_key)
    df['length_secret_key'] = pd.Series(length_secret_key)
    df['length_signature'] = pd.Series(length_signature)

    list_df.append(df)

all_df = pd.concat(list_df)

all_df = all_df.set_index('sig_mechanism')

print(all_df)

all_df.to_csv('sig_mechanism_sizes.csv', index=True)

print('File sig_mechanism_sizes.csv was created')