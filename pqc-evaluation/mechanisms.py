KEM_MECHANISMS =  {
    "mlkem": {
        "include": ["ml-kem"],
    },
    "kyber": {
        "include": ["kyber"],
    },
    "hqc": {
        "include": ["hqc"],
    },
    "bike": {
        "include": ["bike"],
    },
    "mceliece": {
        "include": ["classic-mceliece"],
        "exclude": ["f"]
    },
    "mceliece-f": {
        "include": ["classic-mceliece", "f"],
    },
    "sntrup": {
        "include": ["sntrup"],
    },
    "frodo-aes": {
        "include": ["frodokem", "aes"],
    },
    "frodo-shake": {
        "include": ["frodokem", "shake"],
    },
}

SIG_MECHANISMS = {
    "mldsa": {
        "include": ["ml-dsa"]
    },
    "dilithium": {
        "include": ["dilithium"]
    },
    "sphincs-sha-s": {
        "include": ["sphincs", "sha2", "s"],
        "exclude": ["f"]
    },
    "sphincs-sha-f": {
        "include": ["sphincs", "sha2", "f"],
        # "exclude": ["s"]
    },
    "sphincs-shake-s": {
        "include": ["sphincs", "shake", "s"],
        "exclude": ["f"]
    },
    "sphincs-shake-f": {
        "include": ["sphincs", "shake", "f"],
        # "exclude": ["s"]
    },
    "falcon": {
        "include": ["falcon"],
        "exclude": ["padded"]
    },
    "falcon-padded": {
        "include": ["falcon", "padded"]
    },
    "mayo": {
        "include": ["mayo"],
    },
    "cross-rsdp-small": {
        "include": ["cross", "rsdp", "small"],
        "exclude": ["rsdpg"]
    },
    "cross-rsdpg-small": {
        "include": ["cross", "rsdpg", "small"],
        # "exclude": ["rsdp"]
    },
    "cross-rsdp-balanced": {
        "include": ["cross", "rsdp", "balanced"],
        "exclude": ["rsdpg"]
    },
    "cross-rsdpg-balanced": {
        "include": ["cross", "rsdpg", "balanced"],
        # "exclude": ["rsdp"]
    },
    "cross-rsdp-fast": {
        "include": ["cross", "rsdp", "fast"],
        "exclude": ["rsdpg"]
    },
    "cross-rsdpg-fast": {
        "include": ["cross", "rsdpg", "fast"],
        # "exclude": ["rsdp"]
    },
}