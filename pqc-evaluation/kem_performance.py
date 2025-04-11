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
    # print("Enabled KEM mechanisms:")
    # kems = oqs.get_enabled_kem_mechanisms()
    # pprint(kems, compact=True)

    # Create client and server with sample KEM mechanisms
    # kemalg = "Kyber512"

    print(oqs.get_enabled_kem_mechanisms())
    # ['Kyber512', 'Kyber768', 'Kyber1024']
    for kem_mechanism in oqs.get_enabled_kem_mechanisms(): 
        
        print(kem_mechanism)
        
        generate_keypair_times = []
        encrypt_times = []
        decrypt_times = []
        
        
        df = pd.DataFrame({
            'kem_mechanism': [],
            'generate_keypair_times': [],
            'encrypt_times': [],
            'decrypt_times': []
        })


        df['kem_mechanism'] = pd.Series([kem_mechanism] * int(sys.argv[1]))
    
        for i in range(int(sys.argv[1])):

            with oqs.KeyEncapsulation(kem_mechanism) as client:
                with oqs.KeyEncapsulation(kem_mechanism) as server:
    
                    # Client generates its keypair
                    start_generate_keypair = time.time()
                    public_key_client = client.generate_keypair()
                    end_generate_keypair = time.time()

                    # print(len(public_key_client))

                    generate_keypair_times.append(end_generate_keypair - start_generate_keypair)

                    # Optionally, the secret key can be obtained by calling export_secret_key()
                    # and the client can later be re-instantiated with the key pair:
                    # secret_key_client = client.export_secret_key()

                    # Store key pair, wait... (session resumption):
                    # client = oqs.KeyEncapsulation(kemalg, secret_key_client)

                    # The server encapsulates its secret using the client's public key
                    start_encrypt = time.time()
                    ciphertext, shared_secret_server = server.encap_secret(public_key_client)
                    end_encrypt = time.time()

                    encrypt_times.append(end_encrypt - start_encrypt)

                    # The client decapsulates the server's ciphertext to obtain the shared secret
                    start_decrypt = time.time()
                    shared_secret_client = client.decap_secret(ciphertext)
                    end_decrypt = time.time()
                    
                    decrypt_times.append(end_decrypt - start_decrypt)

                    # print(f"{shared_secret_client == shared_secret_server}")
                    
                    # print(
                    #     "\nShared secretes coincide:", shared_secret_client == shared_secret_server
                    # )


        df['generate_keypair_times'] = pd.Series(generate_keypair_times)
        df['encrypt_times'] = pd.Series(encrypt_times)
        df['decrypt_times'] = pd.Series(decrypt_times)

       
        list_df.append(df)

    all_df = pd.concat(list_df)

    all_df = all_df.set_index('kem_mechanism')

    print(all_df)
    
    all_df.to_csv('kem_mechanism_times.csv', index=True)

    print('File kem_mechanism_times.csv was created')

if __name__ == '__main__':
    main()