from time import time
import pandas as pd
import oqs

def kem_evaluation_times(variant, number):
    
    times_generate_keypair, times_encrypt, times_decrypt = [], [], []

    for i in range(number):
        
        with oqs.KeyEncapsulation(variant) as client, oqs.KeyEncapsulation(variant) as server:
            
            # Client generates its keypair
            start_generate_keypair = time()
            public_key_client = client.generate_keypair()
            end_generate_keypair = time()

            times_generate_keypair.append(end_generate_keypair - start_generate_keypair)

            # Optionally, the secret key can be obtained by calling export_secret_key()
            # and the client can later be re-instantiated with the key pair:
            # secret_key_client = client.export_secret_key()

            # Store key pair, wait... (session resumption):
            # client = oqs.KeyEncapsulation(kemalg, secret_key_client)

            # The server encapsulates its secret using the client's public key
            start_encrypt = time()
            ciphertext, shared_secret_server = server.encap_secret(public_key_client)
            end_encrypt = time()

            times_encrypt.append(end_encrypt - start_encrypt)

            # The client decapsulates the server's ciphertext to obtain the shared secret
            start_decrypt = time()
            shared_secret_client = client.decap_secret(ciphertext)
            end_decrypt = time()
            
            times_decrypt.append(end_decrypt - start_decrypt)

    return pd.DataFrame({
        'variant': [variant] * number,
        'generate_keypair': times_generate_keypair,
        'encrypt': times_encrypt,
        'decrypt': times_decrypt
    })
    
def kem_evaluation_sizes(variant):

    with oqs.KeyEncapsulation(variant) as client:
        # print(client.details)

        return {
            'variant': variant, 
            'ind_cca2': client.details['is_ind_cca'], 
            'claimed_nist_level': client.details['claimed_nist_level'], 
            'length_ciphertext': client.details['length_ciphertext'],
            'length_public_key': client.details['length_public_key'],
            'length_secret_key': client.details['length_secret_key'],
            'length_shared_secret': client.details['length_shared_secret']
        }

