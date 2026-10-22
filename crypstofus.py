#!/usr/bin/env python3
import os
import json
import base64
import random
import secrets
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# =====================================================================
# MÓDULO 1: ARITMÉTICA MODULAR (Rabin-Miller)
# =====================================================================
def miller_rabin(n, k=5):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def modulo_primos():
    print("\n--- 1. ARITMÉTICA MODULAR: Test de Rabin-Miller ---")
    bits = int(input("Ingresá el tamaño en bits (ej. 1024, 2048): "))
    print(f"[*] Generando primo seguro de {bits} bits...")
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1
        if miller_rabin(num, 40):
            print(f"\n[+] Primo encontrado:\n{num}")
            break

# =====================================================================
# MÓDULO 2: DIFFIE-HELLMAN (Intercambio Seguro - RECUPERADO)
# =====================================================================
def dh_exchange(p, g, private_key):
    return pow(g, private_key, p)

def dh_shared_secret(public_received, private_key, p):
    return pow(public_received, private_key, p)

def modulo_diffie_hellman():
    print("\n--- 2. DIFFIE-HELLMAN: Intercambio de Claves Matemático ---")
    print("[*] Simulando parámetros públicos (P y G)...")
    # En la vida real, P es un primo de 2048 bits. Usamos uno chico para el ejemplo.
    p = 23  # Módulo primo público
    g = 5   # Base pública
    
    print(f"Parámetros públicos en la red -> P: {p}, G: {g}")
    
    priv_a = int(input("Ingresá la clave privada de ALICE (ej. 4): "))
    priv_b = int(input("Ingresá la clave privada de BOB (ej. 3): "))
    
    pub_a = dh_exchange(p, g, priv_a)
    pub_b = dh_exchange(p, g, priv_b)
    
    print(f"\n[+] Alice envía a la red su clave pública: {pub_a}")
    print(f"[+] Bob envía a la red su clave pública: {pub_b}")
    
    secreto_alice = dh_shared_secret(pub_b, priv_a, p)
    secreto_bob = dh_shared_secret(pub_a, priv_b, p)
    
    print("\n[!] Generando secreto compartido matemáticamente...")
    print(f"Secreto calculado por Alice: {secreto_alice}")
    print(f"Secreto calculado por Bob:   {secreto_bob}")
    if secreto_alice == secreto_bob:
        print("[+] ¡ÉXITO! Ambos llegaron al mismo secreto sin enviarlo por la red.")

# =====================================================================
# MÓDULOS 3 y 4: CRIPTOGRAFÍA HÍBRIDA (RSA + AES-GCM + OAEP)
# =====================================================================
def modulo_cifrado_hibrido():
    print("\n--- 3. CIFRADO HÍBRIDO (AES-GCM blindado con RSA) ---")
    infile = input("Ruta del archivo a cifrar (ej. mensaje.txt): ")
    pubkey = input("Ruta de la llave pública RSA (.pem): ")
    outfile = input("Nombre del archivo de salida (ej. secreto.json): ")
    
    public_key = serialization.load_pem_public_key(Path(pubkey).read_bytes())
    aes_key = secrets.token_bytes(32)
    aesgcm = AESGCM(aes_key)
    
    plaintext = Path(infile).read_bytes()
    nonce = secrets.token_bytes(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    
    encrypted_aes_key = public_key.encrypt(
        aes_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    
    Path(outfile).write_text(json.dumps({
        "encrypted_aes_key_b64": base64.b64encode(encrypted_aes_key).decode('utf-8'),
        "nonce_b64": base64.b64encode(nonce).decode('utf-8'),
        "ciphertext_b64": base64.b64encode(ciphertext).decode('utf-8')
    }), encoding="utf-8")
    print(f"\n[+] Archivo híbrido generado con éxito en: {outfile}")

def modulo_descifrado_hibrido():
    print("\n--- 4. DESCIFRADO HÍBRIDO (El candado inverso) ---")
    infile = input("Ruta del archivo JSON cifrado (ej. secreto.json): ")
    privkey = input("Ruta de la llave privada RSA (.pem): ")
    outfile = input("Nombre del archivo descifrado de salida: ")
    
    private_key = serialization.load_pem_private_key(Path(privkey).read_bytes(), password=None)
    package = json.loads(Path(infile).read_text(encoding="utf-8"))
    
    encrypted_aes_key = base64.b64decode(package["encrypted_aes_key_b64"])
    nonce = base64.b64decode(package["nonce_b64"])
    ciphertext = base64.b64decode(package["ciphertext_b64"])
    
    aes_key = private_key.decrypt(
        encrypted_aes_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    
    plaintext = AESGCM(aes_key).decrypt(nonce, ciphertext, None)
    Path(outfile).write_bytes(plaintext)
    print(f"\n[+] Archivo descifrado con integridad verificada en: {outfile}")

# =====================================================================
# MÓDULOS 5 a 8: KDF, CHACHA20, HASHES Y ECC
# =====================================================================
def modulo_kdf_pesado():
    print("\n--- 5. KDF LENTO: Argon2 y PBKDF2 (Resistencia Cuántica) ---")
    password = input("Ingresá la contraseña a proteger: ").encode('utf-8')
    salt = secrets.token_bytes(16)
    
    key_argon = Argon2id(salt=salt, length=32, iterations=3, lanes=4, memory_cost=65536).derive(password)
    key_pbkdf2 = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600000).derive(password)
    
    print("\n[+] Salt generado (Base64):", base64.b64encode(salt).decode())
    print("[+] Llave Argon2id (Hex):", key_argon.hex())
    print("[+] Llave PBKDF2-600k (Hex):", key_pbkdf2.hex())

def modulo_descifrado_chacha20():
    print("\n--- 6b. DESCIFRADO SIMÉTRICO: ChaCha20-Poly1305 ---")
    try:
        key_b64 = input("Ingresá la Llave (Base64): ")
        nonce_b64 = input("Ingresá el Nonce (Base64): ")
        ciphertext_b64 = input("Ingresá el Mensaje Cifrado (Base64): ")
        
        # Traducimos de Base64 a bytes puros
        key = base64.b64decode(key_b64)
        nonce = base64.b64decode(nonce_b64)
        ciphertext = base64.b64decode(ciphertext_b64)
        
        # Matemática inversa y verificación de integridad
        plaintext = ChaCha20Poly1305(key).decrypt(nonce, ciphertext, None)
        
        print("\n[+] ¡Candado abierto con éxito! La integridad fue verificada.")
        print("[+] Mensaje original:", plaintext.decode('utf-8'))
    except Exception as e:
        print("\n[!] Error de seguridad: El mensaje fue alterado, la llave es incorrecta o faltan datos.")

def modulo_hashes_rapidos():
    print("\n--- 7. HASHES RÁPIDOS: SHA3 y BLAKE2 ---")
    texto = input("Ingresá el texto: ").encode('utf-8')
    hash_sha3 = hashes.Hash(hashes.SHA3_256())
    hash_sha3.update(texto)
    hash_blake = hashes.Hash(hashes.BLAKE2b(64))
    hash_blake.update(texto)
    print("\n[+] SHA3-256 (Hex):", hash_sha3.finalize().hex())
    print("[+] BLAKE2b-512 (Hex):", hash_blake.finalize().hex())

def modulo_ecc():
    print("\n--- 8. ASIMÉTRICO MODERNO: Curvas Elípticas (ECC) ---")
    private_key = ec.generate_private_key(ec.SECP256R1())
    pem_priv = private_key.private_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()
    )
    print("\n[+] Clave Privada ECC (NIST P-256):")
    print(pem_priv.decode('utf-8'))

# =====================================================================
# MENÚ PRINCIPAL
# =====================================================================
def menu_principal():
    while True:
        print("\n" + "="*65)
        print("   CRYPSTOFUS v7.0 - SUITE CRIPTOGRÁFICA INDUSTRIAL (UGR)")
        print("="*65)
        print("1. Aritmética Modular   -> Generar Primos (Rabin-Miller)")
        print("2. Diffie-Hellman       -> Intercambio Seguro de Claves")
        print("3. Cifrado Híbrido      -> Encriptar (RSA + AES-GCM)")
        print("4. Descifrado Híbrido   -> Desencriptar JSON")
        print("5. KDF Pesado           -> Proteger contraseñas (Argon2)")
        print("6. Cifrar ChaCha20      -> Cifrado Simétrico Móvil")
        print("7. Descifrar ChaCha20   -> Recuperar Mensaje Simétrico")
        print("8. Hashes Rápidos       -> SHA3 / BLAKE2 (Integridad)")
        print("9. Asimétrico Moderno   -> Curvas Elípticas (ECC)")
        print("10. Salir")
        print("="*65)
        
        opcion = input("\n[?] Seleccioná un módulo (1-10): ")
        clear_screen()
        
        if opcion == '1': modulo_primos()
        elif opcion == '2': modulo_diffie_hellman()
        elif opcion == '3': modulo_cifrado_hibrido()
        elif opcion == '4': modulo_descifrado_hibrido()
        elif opcion == '5': modulo_kdf_pesado()
        elif opcion == '6': modulo_chacha20()
        elif opcion == '7': modulo_descifrado_chacha20()
        elif opcion == '8': modulo_hashes_rapidos()
        elif opcion == '9': modulo_ecc()
        elif opcion == '10': 
            print("Cerrando Crypstofus. ¡Excelente trabajo!")
            break
        else: print("[!] Opción inválida.")
        
        input("\n[Presioná ENTER para volver al menú principal...]")
        clear_screen()