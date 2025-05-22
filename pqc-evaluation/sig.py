from time import time
import pandas as pd
import oqs

def time_evaluation(variant, number):

    time_keypair, time_sign, time_verify = [], [], []

    message = "This is the message to sign".encode()

    for i in range(number):

        with oqs.Signature(variant) as signer, oqs.Signature(variant) as verifier:

            # Signer generates its keypair
            start_keypair = time()
            signer_public_key = signer.generate_keypair()
            end_keypair = time()

            time_keypair.append(end_keypair - start_keypair)

            # Optionally, the secret key can be obtained by calling export_secret_key()
            # and the signer can later be re-instantiated with the key pair:
            # secret_key = signer.export_secret_key()

            # Store key pair, wait... (session resumption):
            # signer = oqs.Signature(sigalg, secret_key)

            # Signer signs the message
            start_sign = time()
            signature = signer.sign(message)
            end_sign = time()

            time_sign.append(end_sign - start_sign)

            # Verifier verifies the signature
            start_verify = time()
            is_valid = verifier.verify(message, signature, signer_public_key)
            end_verify = time()

            time_verify.append(end_verify - start_verify)

            # print("\nValid signature?", is_valid)

    return pd.DataFrame({
        'variant': [variant] * number,
        'keypair': time_keypair,
        'sign': time_sign,
        'verify': time_verify
    })

def size_evaluation(variant):
    
    with oqs.Signature(variant) as sig:
        return {
            'variant': variant,
            'nist_level': sig.details['claimed_nist_level'], 
            'public_key': sig.details['length_public_key'],
            'secret_key': sig.details['length_secret_key'],
            'signature': sig.details['length_signature']
        }