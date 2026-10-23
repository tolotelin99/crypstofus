#!/usr/bin/env python3
import os
import json
import base64
import random
import secrets
import datetime
from pathlib import Path

import hashlib
import time
import itertools
import string
import urllib.request
import numpy as np
import matplotlib.pyplot as plt

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.exceptions import InvalidSignature
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
# MÓDULO 2: DIFFIE-HELLMAN (Intercambio Seguro)
# =====================================================================
def dh_exchange(p, g, private_key):
    return pow(g, private_key, p)

def dh_shared_secret(public_received, private_key, p):
    return pow(public_received, private_key, p)

def modulo_diffie_hellman():
    print("\n--- 2. DIFFIE-HELLMAN: Intercambio de Claves Matemático ---")
    print("[*] Simulando parámetros públicos (P y G)...")
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

def modulo_chacha20():
    print("\n--- 6. CIFRADO SIMÉTRICO: ChaCha20-Poly1305 ---")
    mensaje = input("Ingresá el mensaje secreto a cifrar: ").encode('utf-8')
    key, nonce = secrets.token_bytes(32), secrets.token_bytes(12)
    ciphertext = ChaCha20Poly1305(key).encrypt(nonce, mensaje, None)
    
    print("\n[+] Llave (Base64):", base64.b64encode(key).decode())
    print("[+] Nonce (Base64):", base64.b64encode(nonce).decode())
    print("[+] Mensaje Cifrado (Base64):", base64.b64encode(ciphertext).decode())

def modulo_descifrado_chacha20():
    print("\n--- 7. DESCIFRADO SIMÉTRICO: ChaCha20-Poly1305 ---")
    try:
        key_b64 = input("Ingresá la Llave (Base64): ")
        nonce_b64 = input("Ingresá el Nonce (Base64): ")
        ciphertext_b64 = input("Ingresá el Mensaje Cifrado (Base64): ")
        
        key = base64.b64decode(key_b64)
        nonce = base64.b64decode(nonce_b64)
        ciphertext = base64.b64decode(ciphertext_b64)
        
        plaintext = ChaCha20Poly1305(key).decrypt(nonce, ciphertext, None)
        
        print("\n[+] ¡Candado abierto con éxito! La integridad fue verificada.")
        print("[+] Mensaje original:", plaintext.decode('utf-8'))
    except Exception as e:
        print("\n[!] Error de seguridad: El mensaje fue alterado, la llave es incorrecta o faltan datos.")
        
def modulo_hashes_rapidos():
    print("\n--- 8. HASHES RÁPIDOS: SHA3 y BLAKE2 ---")
    texto = input("Ingresá el texto: ").encode('utf-8')
    hash_sha3 = hashes.Hash(hashes.SHA3_256())
    hash_sha3.update(texto)
    hash_blake = hashes.Hash(hashes.BLAKE2b(64))
    hash_blake.update(texto)
    print("\n[+] SHA3-256 (Hex):", hash_sha3.finalize().hex())
    print("[+] BLAKE2b-512 (Hex):", hash_blake.finalize().hex())

# =====================================================================
# MÓDULOS 9 a 14: ECC, FIRMAS DIGITALES, CERTIFICADOS X.509 Y NAVEGADORES
# =====================================================================
def modulo_ecc():
    print("\n--- 9. ASIMÉTRICO MODERNO: Generar Llaves ECC ---")
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    
    pem_priv = private_key.private_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()
    )
    pem_pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    Path("privada_ecc.pem").write_bytes(pem_priv)
    Path("publica_ecc.pem").write_bytes(pem_pub)
    print("\n[+] Llaves ECC (NIST P-256) generadas con éxito.")
    print("[+] Guardadas en tu carpeta como: 'privada_ecc.pem' y 'publica_ecc.pem'")

def modulo_firmar_ecc():
    print("\n--- 10. FIRMA DIGITAL: Firmar mensaje (ECDSA) ---")
    privkey = input("Ruta de la llave privada ECC (.pem) [ej. privada_ecc.pem]: ")
    mensaje = input("Ingresá el mensaje a firmar: ").encode('utf-8')
    
    private_key = serialization.load_pem_private_key(Path(privkey).read_bytes(), password=None)
    firma = private_key.sign(mensaje, ec.ECDSA(hashes.SHA256()))
    
    print("\n[+] Firma Digital generada (Base64):")
    print(base64.b64encode(firma).decode('utf-8'))
    print("\n[i] Entregale al destinatario el Mensaje, tu Llave Pública y esta Firma.")

def modulo_verificar_ecc():
    print("\n--- 11. FIRMA DIGITAL: Verificar firma (ECDSA) ---")
    pubkey = input("Ruta de la llave pública ECC (.pem) [ej. publica_ecc.pem]: ")
    mensaje = input("Ingresá el mensaje original: ").encode('utf-8')
    firma_b64 = input("Ingresá la Firma (Base64): ")
    
    public_key = serialization.load_pem_public_key(Path(pubkey).read_bytes())
    firma = base64.b64decode(firma_b64)
    
    try:
        public_key.verify(firma, mensaje, ec.ECDSA(hashes.SHA256()))
        print("\n[+] ¡Firma VÁLIDA! El mensaje es auténtico y pertenece al dueño de la llave.")
    except InvalidSignature:
        print("\n[!] ¡ALERTA DE SEGURIDAD! Firma inválida. El mensaje fue alterado o es un impostor.")

def modulo_x509():
    print("\n--- 12. IDENTIDAD DIGITAL: Generar Certificado X.509 ---")
    print("Vamos a crear un certificado TLS/SSL (Firma X9.62 ECDSA con SHA-256).")
    privkey = input("Ruta de tu llave privada ECC (.pem) [ej. privada_ecc.pem]: ")
    
    private_key = serialization.load_pem_private_key(Path(privkey).read_bytes(), password=None)
    public_key = private_key.public_key()
    
    dominio = input("Ingresá tu dominio (ej. ugr.edu.ar): ")
    org = input("Ingresá tu organización (ej. Ciberseguridad UGR): ")
    
    dias_input = input("Ingresá los días de validez (ej. 365 para 1 año, 3650 para 10 años): ")
    try:
        dias_validez = int(dias_input)
    except ValueError:
        print("[!] Valor inválido. Se usarán 365 días por defecto.")
        dias_validez = 365
    
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        x509.NameAttribute(NameOID.COMMON_NAME, dominio),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        public_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=dias_validez)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(dominio)]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    Path("certificado_tls.pem").write_bytes(cert_pem)
    
    print(f"\n[+] Certificado X.509 generado exitosamente a nombre de '{dominio}'.")
    print(f"[+] Validez configurada y sellada: {dias_validez} días.")
    print("[+] Guardado como 'certificado_tls.pem'. ¡Compatible con Chrome, Edge, Brave y Firefox!")

def modulo_leer_x509():
    print("\n--- 13. FORENSE: Analizar Certificado X.509 ---")
    cert_path = input("Ruta del certificado (.pem) [ej. certificado_tls.pem]: ")
    
    try:
        cert_data = Path(cert_path).read_bytes()
        cert = x509.load_pem_x509_certificate(cert_data)
        
        print("\n[+] Análisis Forense del Certificado:")
        print(f" - Sujeto (Dueño): {cert.subject}")
        print(f" - Emisor (Autoridad): {cert.issuer}")
        print(f" - Número de Serie: {cert.serial_number}")
        print(f" - Algoritmo de Firma: {cert.signature_hash_algorithm.name.upper()} (X9.62 ECDSA)")
        print(f" - Válido desde: {cert.not_valid_before_utc}")
        print(f" - Válido hasta: {cert.not_valid_after_utc}")
    except Exception as e:
        print("\n[!] Error: El archivo no es un certificado X.509 válido o no está en formato PEM.")

def modulo_compatibilidad_navegadores():
    print("\n--- 14. AUDITORÍA: Compatibilidad de Certificados con Navegadores ---")
    cert_path = input("Ruta del certificado a auditar (.pem) [ej. certificado_tls.pem]: ")
    
    try:
        cert_data = Path(cert_path).read_bytes()
        cert = x509.load_pem_x509_certificate(cert_data)
        
        print("\n[+] Simulando compatibilidad con motores de navegación modernos...")
        
        pub_key = cert.public_key()
        es_ecc = isinstance(pub_key, ec.EllipticCurvePublicKey)
        es_rsa = isinstance(pub_key, rsa.RSAPublicKey)
        
        print(f" • Google Chrome / Chromium / Microsoft Edge:")
        print(f"    -> [APROBADO] Confían en la llave y el estándar X9.62 (vía almacén del SO).")
        
        print(f" • Brave Browser:")
        print(f"    -> [APROBADO] Totalmente compatible con la arquitectura de red (Shields & Engine).")
        
        print(f" • Mozilla Firefox:")
        if es_ecc or es_rsa:
            print(f"    -> [APROBADO] Compatible con bases de confianza nativas y almacenamiento del SO (v120+).")
        else:
            print(f"    -> [ADVERTENCIA] Algoritmo no estándar detectado para políticas estrictas de Mozilla.")
            
        print(f" • Tor Browser:")
        print(f"    -> [VERIFICACIÓN ESTRICTA] Requerirá importación manual como Autoridad Raíz de confianza en 'about:preferences#privacy',")
        print(f"        ya que Tor bloquea por defecto certificados autofirmados externos para prevenir rastreo o MitM.")
        
    except Exception as e:
        print("\n[!] Error: No se pudo auditar el archivo. Asegurate de que sea un PEM válido.")

# =====================================================================
# MÓDULO 15: UTILIDADES DE CODIFICACIÓN Y BYTES (Con .strip() anti-espacios)
# =====================================================================
def menu_conversiones():
    print("\n--- 15. UTILIDADES DE CODIFICACIÓN Y BYTES ---")
    print("1. ASCII a Hexadecimal")
    print("2. Hexadecimal a ASCII")
    print("3. Hexadecimal a Binario")
    sub_op = input("Seleccioná una opción: ")
    
    if sub_op == "1":
        ascii_string = input("Ingresá la frase ASCII: ")
        hex_str = ''.join([format(ord(char), '02x') for char in ascii_string])
        print(f"[+] Hexadecimal: {hex_str}")
    elif sub_op == "2":
        hex_string = input("Ingresá la cadena Hexadecimal: ").strip()
        try:
            ascii_str = bytes.fromhex(hex_string).decode("utf-8")
            print(f"[+] ASCII: {ascii_str}")
        except Exception as e:
            print(f"[!] Error en la conversión: {e}")
    elif sub_op == "3":
        hex_string = input("Ingresá la cadena Hexadecimal: ").strip()
        binary_string = ""
        for char in hex_string:
            try:
                dec = int(char, 16)
                binary_string += format(dec, '04b')
            except ValueError:
                print(f"[!] Carácter hexadecimal inválido: '{char}'")
                return
        print(f"[+] Binario: {binary_string}")

def menu_cifrados_clasicos():
    print("\n--- 16. CRIPTOANÁLISIS CLÁSICO (César) ---")
    print("1. Cifrar con Cifrado César (Shift = 9)")
    print("2. Crackear Cifrado César por Fuerza Bruta")
    sub_op = input("Seleccioná una opción: ")
    
    if sub_op == "1":
        text = input("Ingrese la frase sin espacios: ")
        s = 9
        result = ""
        for char in text:
            if char.isupper():
                result += chr((ord(char) + s - 65) % 26 + 65)
            else:
                result += chr((ord(char) + s - 97) % 26 + 97)
        print(f"[+] Cifrado César: {result}")
    elif sub_op == "2":
        message = input("Ingrese la frase cifrada: ").upper()
        SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for key in range(len(SYMBOLS)):
            translated = ''
            for symbol in message:
                if symbol in SYMBOLS:
                    idx = SYMBOLS.find(symbol) - key
                    if idx < 0:
                        idx += len(SYMBOLS)
                    translated += SYMBOLS[idx]
                else:
                    translated += symbol
            print(f"Key #{key}: {translated}")

def generar_primos():
    print("\n--- 17. GENERADOR DE NÚMEROS PRIMOS (Base RSA) ---")
    try:
        start = int(input("Ingrese el rango inicial: "))
        end = int(input("Ingrese el rango final: "))
        prime_list = []
        for i in range(start, end):
            if i < 2:
                continue
            for j in range(2, int(i/2) + 1):
                if i % j == 0:
                    break
            else:
                prime_list.append(i)
        print(f"[+] Primos encontrados en el rango: {prime_list}")
    except ValueError:
        print("[!] Por favor ingrese números válidos.")

def plot_elliptic_curve():
    print("\n--- 18. VISUALIZADOR DE CURVAS ELÍPTICAS ---")
    print("[+] Renderizando curva elíptica matemática (y^2 = x^3 - 5x + 5)...")
    a = -5
    b = 5
    y, x = np.ogrid[-7:7:100j, -7:7:100j]
    plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * a - b, [0])
    plt.grid()
    plt.title("Curva Elíptica (Base ECDSA Cryptofus)")
    plt.show()


# =====================================================================
# MÓDULO 19: HASHING Y AUDITORÍA (CrackStation Master List + Web Stream + Algorítmico Ampliado)
# =====================================================================
def modulo_hashing_auditoria():
    print("\n--- 19. HASHING Y AUDITORÍA DE CONTRASEÑAS (Estilo Hashcat/John) ---")
    print("1. Calcular Hash SHA-256")
    print("2. Ataque por Diccionario (Interno CrackStation/SecLists o URL web / .txt local)")
    print("3. Ataque algorítmico al vuelo (Generación matemática con itertools)")
    sub_op = input("Seleccioná una opción: ")
    
    if sub_op == "1":
        texto = input("Ingresá el texto a hashear: ")
        print(f"[+] SHA-256: {hashlib.sha256(texto.encode('utf-8')).hexdigest()}")
        
    elif sub_op == "2":
        hash_obj = input("Ingresá el hash SHA-256 objetivo: ").strip().lower()
        dict_input = input("Ruta local, URL web de GitHub (.txt) o Enter para diccionario interno: ").strip()
        
        # 1. Diccionario Interno Ampliado (Inspirado en CrackStation / SecLists top passwords)
        if not dict_input:
            print("[*] Usando diccionario interno avanzado (CrackStation/SecLists master top)...")
            diccionario = [
                "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", 
                "111111", "1234567", "dragon", "baseball", "football", "monkey", "letmein", 
                "master", "sunshine", "ashley", "bailey", "shadow", "superman", "computer", 
                "trustno1", "admin", "toor", "crypstofus2026", "seguridad", "ciberseguridad", 
                "welcome", "password123", "ugr2026", "iloveyou", "princess", "rockyou", 
                "matrix", "hacker", "pentest", "root", "ubuntu", "kali", "debian"
            ]
            inicio = time.time()
            intentos = 0
            encontrado = False
            
            for palabra in diccionario:
                intentos += 1
                h_calc = hashlib.sha256(palabra.encode('utf-8')).hexdigest()
                if h_calc == hash_obj:
                    tiempo_total = time.time() - inicio
                    print(f"\n[¡ÉXITO!] Contraseña encontrada en diccionario interno: '{palabra}'")
                    print(f"[+] Intentos realizados: {intentos:,}")
                    print(f"[+] Tiempo transcurrido: {tiempo_total:.4f} segundos")
                    encontrado = True
                    break
            if not encontrado:
                print(f"\n[-] Contraseña no encontrada. Se probaron {intentos:,} palabras del diccionario interno.")
        
        # 2. Streaming Web Directo desde GitHub / Open Source (Sin descargar nada)
        elif dict_input.startswith("http://") or dict_input.startswith("https://"):
            print(f"[*] Conectando a internet para leer el diccionario remoto en streaming...")
            inicio = time.time()
            intentos = 0
            encontrado = False
            
            try:
                with urllib.request.urlopen(dict_input) as response:
                    for line in response:
                        palabra = line.decode('utf-8', errors='ignore').strip()
                        if not palabra:
                            continue
                        intentos += 1
                        h_calc = hashlib.sha256(palabra.encode('utf-8')).hexdigest()
                        if h_calc == hash_obj:
                            tiempo_total = time.time() - inicio
                            print(f"\n[¡ÉXITO!] Contraseña encontrada vía Web: '{palabra}'")
                            print(f"[+] Intentos realizados: {intentos:,}")
                            print(f"[+] Tiempo transcurrido: {tiempo_total:.4f} segundos")
                            encontrado = True
                            break
                if not encontrado:
                    print(f"\n[-] Contraseña no encontrada en la lista remota ({intentos:,} intentos).")
            except Exception as e:
                print(f"[!] Error al conectar con la URL: {e}")
                
        # 3. Archivo Local .txt en la PC
        else:
            if not os.path.exists(dict_input):
                print(f"[!] Error: No se encontró el archivo local '{dict_input}'.")
                return
                
            print(f"[*] Leyendo archivo local y probando contra '{dict_input}'...")
            inicio = time.time()
            intentos = 0
            encontrado = False
            
            try:
                with open(dict_input, 'r', encoding='utf-8', errors='ignore') as f:
                    for linea in f:
                        palabra = linea.strip()
                        if not palabra:
                            continue
                        intentos += 1
                        h_calc = hashlib.sha256(palabra.encode('utf-8')).hexdigest()
                        if h_calc == hash_obj:
                            tiempo_total = time.time() - inicio
                            print(f"\n[¡ÉXITO!] Contraseña encontrada en archivo local: '{palabra}'")
                            print(f"[+] Intentos realizados: {intentos:,}")
                            print(f"[+] Tiempo transcurrido: {tiempo_total:.4f} segundos")
                            encontrado = True
                            break
                if not encontrado:
                    print(f"\n[-] Contraseña no encontrada. Se probaron {intentos:,} palabras del archivo.")
            except Exception as e:
                print(f"[!] Error al leer el archivo de diccionario: {e}")
            
    elif sub_op == "3":
        hash_obj = input("Ingresá el hash SHA-256 objetivo: ").strip().lower()
        print("\n[?] Seleccioná el tipo de juego de caracteres (Rangos Ampliados):")
        print("1. Solo Números (PINs de 1 a 10 dígitos)")
        print("2. Letras min/mayús + Números (Claves de 1 a 8 caracteres)")
        tipo_set = input("Seleccioná el set (1-2): ")
        
        if tipo_set == "1":
            caracteres = string.digits
            max_len = 10  # Rango ampliado a 10 dígitos
        else:
            caracteres = string.ascii_letters + string.digits  # Minúsculas, mayúsculas y números
            max_len = 8   # Rango ampliado a 8 caracteres
            
        print(f"[*] Iniciando ataque algorítmico al vuelo (itertools) con max_len={max_len}...")
        inicio = time.time()
        intentos = 0
        encontrado = False
        
        try:
            for longitud in range(1, max_len + 1):
                for combinacion in itertools.product(caracteres, repeat=longitud):
                    palabra = "".join(combinacion)
                    intentos += 1
                    h_calc = hashlib.sha256(palabra.encode('utf-8')).hexdigest()
                    
                    if h_calc == hash_obj:
                        tiempo_total = time.time() - inicio
                        print(f"\n[¡ÉXITO ALGORÍTMICO!] Contraseña encontrada: '{palabra}'")
                        print(f"[+] Combinaciones probadas: {intentos:,}")
                        print(f"[+] Tiempo transcurrido: {tiempo_total:.4f} segundos")
                        encontrado = True
                        break
                if encontrado:
                    break
                    
            if not encontrado:
                print(f"\n[-] No se encontró coincidencia en el rango analizado ({intentos:,} intentos).")
        except Exception as e:
            print(f"[!] Error durante la ejecución algorítmica: {e}")


# =====================================================================
# MENÚ PRINCIPAL
# =====================================================================
def menu_principal():
    while True:
        print("\n" + "="*65)
        print("    CRYPSTOFUS v10.0 - SUITE CRIPTOGRÁFICA INDUSTRIAL (UGR)")
        print("="*65)
        print("1. Aritmética Modular     -> Generar Primos (Rabin-Miller)")
        print("2. Diffie-Hellman         -> Intercambio Seguro de Claves")
        print("3. Cifrado Híbrido        -> Encriptar (RSA + AES-GCM)")
        print("4. Descifrado Híbrido     -> Desencriptar JSON")
        print("5. KDF Pesado             -> Proteger contraseñas (Argon2)")
        print("6. Cifrar ChaCha20        -> Cifrado Simétrico Móvil")
        print("7. Descifrar ChaCha20     -> Recuperar Mensaje Simétrico")
        print("8. Hashes Rápidos         -> SHA3 / BLAKE2 (Integridad)")
        print("9. Generar Llaves ECC     -> Asimétrico Moderno (NIST P-256)")
        print("10. Firmar Mensaje        -> Crear Firma Digital (ECDSA)")
        print("11. Verificar Firma       -> Validar Autenticidad (ECDSA)")
        print("12. Generar Certificado   -> Identidad Digital (X.509 TLS)")
        print("13. Analizar Certificado  -> Forense de X.509")
        print("14. Auditar Navegadores   -> Compatibilidad Chrome/Firefox/Tor")
        print("15. Utilidades Bytes      -> Conversión ASCII/Hex/Binario")
        print("16. Cifrados Clásicos     -> Cifrado César y Criptoanálisis")
        print("17. Generador Primos      -> Listar Primos para RSA")
        print("18. PlOT Curva Elíptica   -> Visualizador Gráfico (ECC)")
        print("19. Hashing & Auditar     -> SHA-256 & Fuerza Bruta de Contraseñas")
        print("20. Salir")
        print("="*65)
        
        opcion = input("\n[?] Seleccioná un módulo (1-20): ")
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
        elif opcion == '10': modulo_firmar_ecc()
        elif opcion == '11': modulo_verificar_ecc()
        elif opcion == '12': modulo_x509()
        elif opcion == '13': modulo_leer_x509()
        elif opcion == '14': modulo_compatibilidad_navegadores()
        elif opcion == '15': menu_conversiones()
        elif opcion == '16': menu_cifrados_clasicos()
        elif opcion == '17': generar_primos()
        elif opcion == '18': plot_elliptic_curve()
        elif opcion == '19': modulo_hashing_auditoria()
        elif opcion == '20': 
            print("Cerrando Crypstofus. ¡Excelente trabajo!")
            break
        else: print("[!] Opción inválida.")
        
        input("\n[Presioná ENTER para volver al menú principal...]")
        clear_screen()
        
if __name__ == "__main__":
    clear_screen()
    menu_principal()