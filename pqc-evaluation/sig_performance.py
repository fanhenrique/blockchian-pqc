import pandas as pd
import matplotlib.pyplot as plt
import time
import oqs 
import sys

def main():

    if len(sys.argv) == 2:
        if not sys.argv[1].isdigit(): 
            print(f'Usage: python {sys.argv[0]} <run_numbers>')
            exit()

    list_df = []

    # print("liboqs version:", oqs.oqs_version())
    # print("liboqs-python version:", oqs.oqs_python_version())
    # print("Enabled signature mechanisms:")
    # sigs = oqs.get_enabled_sig_mechanisms()
    # pprint(sigs, compact=True)

    message = "This is the message to sign".encode()

    # Create signer and verifier with sample signature mechanisms
    # sigalg = "Dilithium2"
    
    print(oqs.get_enabled_sig_mechanisms())

    for sig_mechanism in oqs.get_enabled_sig_mechanisms():

        print(sig_mechanism)

        generate_keypair_times = []
        sign_times = []
        verify_times = []
        
        df = pd.DataFrame({
            'sig_mechanism': [],
            'generate_keypair_times': [],
            'sign_times': [],
            'verify_times': []
        })

        df['sig_mechanism'] = pd.Series([sig_mechanism] * int(sys.argv[1]))
    
        for i in range(int(sys.argv[1])):

            with oqs.Signature(sig_mechanism) as signer:
                with oqs.Signature(sig_mechanism) as verifier:

                    # Signer generates its keypair
                    start_generate_keypair = time.time()
                    signer_public_key = signer.generate_keypair()
                    end_generate_keypair = time.time()

                    generate_keypair_times.append(end_generate_keypair - start_generate_keypair)

                    # Optionally, the secret key can be obtained by calling export_secret_key()
                    # and the signer can later be re-instantiated with the key pair:
                    # secret_key = signer.export_secret_key()

                    # Store key pair, wait... (session resumption):
                    # signer = oqs.Signature(sigalg, secret_key)

                    # Signer signs the message
                    start_sign = time.time()
                    signature = signer.sign(message)
                    end_sign = time.time()

                    sign_times.append(end_sign - start_sign)

                    # Verifier verifies the signature
                    start_verify = time.time()
                    is_valid = verifier.verify(message, signature, signer_public_key)
                    end_verify = time.time()

                    verify_times.append(end_verify - start_verify)

                    # print("\nValid signature?", is_valid)


        df['generate_keypair_times'] = pd.Series(generate_keypair_times)
        df['sign_times'] = pd.Series(sign_times)
        df['verify_times'] = pd.Series(verify_times)

       
        list_df.append(df)

    all_df = pd.concat(list_df)

    all_df = all_df.set_index('sig_mechanism')

    print(all_df)
    
    all_df.to_csv('sig_mechanism_times.csv', index=True)

    print('File sig_mechanism_times.csv was created')

if __name__ == '__main__':
    main()