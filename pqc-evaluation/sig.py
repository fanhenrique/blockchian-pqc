from time import time
import pandas as pd
import oqs

def times_evaluation(variant, number):

    times_generate_keypair, times_sign, times_verify = [], [], []

    message = "This is the message to sign".encode()

    for i in range(number):

        with oqs.Signature(variant) as signer, oqs.Signature(variant) as verifier:

            # Signer generates its keypair
            start_generate_keypair = time()
            signer_public_key = signer.generate_keypair()
            end_generate_keypair = time()

            times_generate_keypair.append(end_generate_keypair - start_generate_keypair)

            # Optionally, the secret key can be obtained by calling export_secret_key()
            # and the signer can later be re-instantiated with the key pair:
            # secret_key = signer.export_secret_key()

            # Store key pair, wait... (session resumption):
            # signer = oqs.Signature(sigalg, secret_key)

            # Signer signs the message
            start_sign = time()
            signature = signer.sign(message)
            end_sign = time()

            times_sign.append(end_sign - start_sign)

            # Verifier verifies the signature
            start_verify = time()
            is_valid = verifier.verify(message, signature, signer_public_key)
            end_verify = time()

            times_verify.append(end_verify - start_verify)

            # print("\nValid signature?", is_valid)

    return pd.DataFrame({
        'variant': [variant] * number,
        'generate_keypair': times_generate_keypair,
        'sign': times_sign,
        'verify': times_verify
    })

def sizes_evaluation(variant):
    
    with oqs.Signature(variant) as sig:
    
        return {
            'variant': variant,
            'claimed_nist_level': sig.details['claimed_nist_level'], 
            'length_public_key': sig.details['length_public_key'],
            'length_secret_key': sig.details['length_secret_key'],
            'length_signature': sig.details['length_signature']
        }