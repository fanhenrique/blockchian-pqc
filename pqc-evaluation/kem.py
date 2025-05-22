from time import time
import pandas as pd
import oqs

def time_evaluation(variant, number):
    
    time_keypair, time_encrypt, time_decrypt = [], [], []

    for i in range(number):
        
        with oqs.KeyEncapsulation(variant) as client, oqs.KeyEncapsulation(variant) as server:
            
            # Client generates its keypair
            start_keypair = time()
            public_key_client = client.generate_keypair()
            end_keypair = time()

            time_keypair.append(end_keypair - start_keypair)

            # Optionally, the secret key can be obtained by calling export_secret_key()
            # and the client can later be re-instantiated with the key pair:
            # secret_key_client = client.export_secret_key()

            # Store key pair, wait... (session resumption):
            # client = oqs.KeyEncapsulation(kemalg, secret_key_client)

            # The server encapsulates its secret using the client's public key
            start_encrypt = time()
            ciphertext, shared_secret_server = server.encap_secret(public_key_client)
            end_encrypt = time()

            time_encrypt.append(end_encrypt - start_encrypt)

            # The client decapsulates the server's ciphertext to obtain the shared secret
            start_decrypt = time()
            shared_secret_client = client.decap_secret(ciphertext)
            end_decrypt = time()
            
            time_decrypt.append(end_decrypt - start_decrypt)

    return pd.DataFrame({
        'variant': [variant] * number,
        'keypair': time_keypair,
        'encrypt': time_encrypt,
        'decrypt': time_decrypt
    })

def size_evaluation(variant):

    with oqs.KeyEncapsulation(variant) as kem:
        return {
            'variant': variant,
            'nist_level': kem.details['claimed_nist_level'], 
            'ciphertext': kem.details['length_ciphertext'],
            'public_key': kem.details['length_public_key'],
            'secret_key': kem.details['length_secret_key'],
            'shared_secret': kem.details['length_shared_secret']
        }

