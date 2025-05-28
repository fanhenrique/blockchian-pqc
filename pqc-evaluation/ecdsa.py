from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
from time import time
import random
import string
import pandas as pd

def time_evaluation(variant, runs, warm_up):

    curves = {
        "P-256": ec.SECP256R1(),
        "P-384": ec.SECP384R1(),
        "P-521": ec.SECP521R1(),
    }

    if variant not in curves:
        raise ValueError(f"Unknown variant {variant}. Available: {list(curves.keys())}")

    curve = curves[variant]

    # Warm up
    for i in range(warm_up):

        message = ''.join(random.choices(string.ascii_letters + string.digits, k=60)).encode("utf-8")

        sk = ec.generate_private_key(curve)
        pk = sk.public_key()

        signature = sk.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )

        try:
            pk.verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256())
            )
        except InvalidSignature:
            print(f"WARNING: Verification failed at iteration {i}!")
        

    time_keypair, time_sign, time_verify = [], [], []
    
    # Runs
    for i in range(runs):

        message = ''.join(random.choices(string.ascii_letters + string.digits, k=60)).encode("utf-8")

        start_keypair = time()
        sk = ec.generate_private_key(curve)
        pk = sk.public_key()
        end_keypair = time()

        time_keypair.append((end_keypair - start_keypair) * 1000)

        start_sign=time()
        signature = sk.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )
        end_sign=time()
    
        time_sign.append((end_sign - start_sign) * 1000)

        try:
            start_verify=time()
            pk.verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256())
            )
            end_verify=time()
        except InvalidSignature:
            print(f"WARNING: Verification failed at iteration {i}!")
        
        time_verify.append((end_verify - start_sign) * 1000)

    return pd.DataFrame({
        'variant': [variant] * runs,
        'keypair': time_keypair,
        'sign': time_sign,
        'verify': time_verify
    })
