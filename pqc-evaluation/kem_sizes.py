# Key encapsulation Python example

import pandas as pd
import matplotlib.pyplot as plt

import oqs
from pprint import pprint

# print("liboqs version:", oqs.oqs_version())
# print("liboqs-python version:", oqs.oqs_python_version())
# print("Enabled KEM mechanisms:")
# kems = oqs.get_enabled_kem_mechanisms()
# pprint(kems, compact=True)

# Create client and server with sample KEM mechanisms
# kemalg = "Kyber512"


list_df = []

for kemalg in oqs.get_enabled_kem_mechanisms():

    kem_mechanism = []
    is_ind_cca = []
    claimed_nist_level = []
    length_ciphertext = []
    length_public_key = []
    length_secret_key = []
    length_shared_secret = []

    df = pd.DataFrame({
        'kem_mechanism': [], 
        'is_ind_cca': [], 
        'claimed_nist_level': [], 
        'length_ciphertext': [],
        'length_public_key': [],
        'length_secret_key': [],
        'length_shared_secret': []
    })

    with oqs.KeyEncapsulation(kemalg) as client:
        with oqs.KeyEncapsulation(kemalg) as server:
            # print("\nKey encapsulation details:")
            
            # pprint(client.details)
            # print(f"{kemalg},", end='')
            # print(f"{client.details['is_ind_cca']},", end='')
            # print(f"{client.details['claimed_nist_level']},", end='')
            # print(f"{client.details['length_ciphertext']},", end='')
            # print(f"{client.details['length_public_key']},", end='')
            # print(f"{client.details['length_secret_key']},", end='')
            # print(f"{client.details['length_shared_secret']},", end='')

            kem_mechanism.append(kemalg)
            is_ind_cca.append(client.details['is_ind_cca'])
            claimed_nist_level.append(client.details['claimed_nist_level'])
            length_ciphertext.append(client.details['length_ciphertext'])
            length_public_key.append(client.details['length_public_key'])
            length_secret_key.append(client.details['length_secret_key'])
            length_shared_secret.append(client.details['length_shared_secret'])


            # Client generates its keypair
            public_key_client = client.generate_keypair()
            # Optionally, the secret key can be obtained by calling export_secret_key()
            # and the client can later be re-instantiated with the key pair:
            # secret_key_client = client.export_secret_key()

            # Store key pair, wait... (session resumption):
            # client = oqs.KeyEncapsulation(kemalg, secret_key_client)

            # The server encapsulates its secret using the client's public key
            ciphertext, shared_secret_server = server.encap_secret(public_key_client)

            # The client decapsulates the server's ciphertext to obtain the shared secret
            shared_secret_client = client.decap_secret(ciphertext)


            # print(f"{shared_secret_client == shared_secret_server}")
            
            # print(
            #     "\nShared secretes coincide:", shared_secret_client == shared_secret_server
            # )

    df['kem_mechanism'] = pd.Series(kem_mechanism)
    df['is_ind_cca'] = pd.Series(is_ind_cca)
    df['claimed_nist_level'] = pd.Series(claimed_nist_level)
    df['length_ciphertext'] = pd.Series(length_ciphertext)
    df['length_public_key'] = pd.Series(length_public_key)
    df['length_secret_key'] = pd.Series(length_secret_key)
    df['length_shared_secret'] = pd.Series(length_shared_secret)
   
    list_df.append(df)

all_df = pd.concat(list_df)

all_df = all_df.set_index('kem_mechanism')

print(all_df)

all_df.to_csv('kem_mechanism_sizes.csv', index=True)

print('File kem_mechanism_sizes.csv was created')
