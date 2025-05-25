from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
from time import time_ns
import random
import string
import pandas as pd

def time_evaluation(variant, runs):

    curves = {
        "P-256": ec.SECP256R1(),
        "P-384": ec.SECP384R1(),
        "P-521": ec.SECP521R1(),
    }

    if variant not in curves:
        raise ValueError(f"Unknown variant {variant}. Available: {list(curves.keys())}")

    curve = curves[variant]

    time_keypair, time_sign, time_verify = [], [], []

    for i in range(runs):

        message = ''.join(random.choices(string.ascii_letters + string.digits, k=60)).encode("utf-8")

        start_keypair = time_ns()
        sk = ec.generate_private_key(curve)
        pk = sk.public_key()
        end_keypair = time_ns()

        time_keypair.append(end_keypair - start_keypair)

        start_sign=time_ns()
        signature = sk.sign(
            message,
            ec.ECDSA(hashes.SHA256())
        )
        end_sign=time_ns()
    
        time_sign.append(end_sign - start_sign)

        try:
            start_verify=time_ns()
            pk.verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256())
            )
            end_verify=time_ns()    
        except InvalidSignature:
            print(f"WARNING: Verification failed at iteration {i}!")
        
        time_verify.append(end_verify - start_sign)


    return pd.DataFrame({
        'variant': [variant] * runs,
        'keypair': time_keypair,
        'sign': time_sign,
        'verify': time_verify
    })

# curves= [ec.SECP256R1(), ec.SECP384R1(), ec.SECP521R1()]



# time_results = []

# for curve in curves:
#     print(curve.name)
#     time_results.append(time_evaluation(curve, 3))

# df = pd.concat(time_results)

# print(df)

