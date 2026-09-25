import argparse
import base64
import hashlib
import os
from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def codify_operations(text, mode):
  """Operaciones clásicas y codificación."""
  try:
    if mode == "b64-enc":
      return base64.b64encode(text.encode("utf-8")).decode("utf-8")
    elif mode == "b64-dec":
      return base64.b64decode(text.encode("utf-8")).decode("utf-8", errors="ignore")
    elif mode == "hex-enc":
      return text.encode("utf-8").hex()
    elif mode == "hex-dec":
      return bytes.fromhex(text).decode("utf-8", errors="ignore")
  except Exception as e:
    return f"Error: {e}"


def aes_gcm_encrypt(plaintext):
  """Cifrado simétrico moderno de grado industrial (AES-256-GCM)."""
  print("\n[*] Módulo de Cifrado Simétrico (AES-256-GCM):")
  print("-" * 65)
  key = AESGCM.generate_key(bit_length=256)
  aesgcm = AESGCM(key)
  nonce = os.urandom(12)
  
  ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
  
  print(f"    [+] Llave Secreta (Hex) : {key.hex()}")
  print(f"    [+] Nonce (Hex)         : {nonce.hex()}")
  print(f"    [+] Texto Cifrado (Hex) : {ciphertext.hex()}")
  print("    [i] Nota: AES-GCM provee confidencialidad e integridad autenticada.")
  print("-" * 65)


def rsa_asymmetric_operations(message):
  """Cifrado Asimétrico Real con RSA (2048 bits + OAEP padding)."""
  print("\n[*] Módulo de Cifrado Asimétrico (RSA-2048 / OAEP):")
  print("-" * 65)
  private_key = rsa.generate_private_key(
      public_exponent=65537,
      key_size=2048
  )
  public_key = private_key.public_key()

  ciphertext = public_key.encrypt(
      message.encode("utf-8"),
      padding.OAEP(
          mgf=padding.MGF1(algorithm=hashes.SHA256()),
          algorithm=hashes.SHA256(),
          label=None
      )
  )

  decrypted_message = private_key.decrypt(
      ciphertext,
      padding.OAEP(
          mgf=padding.MGF1(algorithm=hashes.SHA256()),
          algorithm=hashes.SHA256(),
          label=None
      )
  )

  print(f"    [+] Mensaje Original    : {message}")
  print(f"    [+] Texto Cifrado (Hex) : {ciphertext.hex()[:60]}... [Truncado]")
  print(f"    [+] Mensaje Descifrado  : {decrypted_message.decode('utf-8')}")
  print("-" * 65)


def generate_hashes(text):
  """Hashes tradicionales y KDF pesado."""
  print("\n[*] Generando huellas y hashes de alta seguridad:")
  print("-" * 65)
  print(f"    [MD5]       : {hashlib.md5(text.encode()).hexdigest()}")
  print(f"    [SHA-256]   : {hashlib.sha256(text.encode()).hexdigest()}")
  print(f"    [SHA-512]   : {hashlib.sha512(text.encode()).hexdigest()}")
  
  salt = os.urandom(16)
  kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=salt,
      iterations=100000,
  )
  heavy_hash = kdf.derive(text.encode())
  print(f"    [Heavy-KDF] : {heavy_hash.hex()} (Sal: {salt.hex()})")
  print("-" * 65)


def elliptic_curve_crypto():
  """Curvas Elípticas (ECC - SECP256R1)."""
  print("\n[*] Módulo de Criptografía de Curva Elíptica (ECC):")
  print("-" * 65)
  private_key = ec.generate_private_key(ec.SECP256R1())
  public_key = private_key.public_key()

  pem_private = private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.PKCS8,
      encryption_algorithm=serialization.NoEncryption()
  )
  pem_public = public_key.public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo
  )

  print("    [+] Llave Privada ECC generada:")
  print(pem_private.decode("utf-8").strip())
  print("\n    [+] Llave Pública ECC correspondiente:")
  print(pem_public.decode("utf-8").strip())
  print("-" * 65)


def post_quantum_simulation(text):
  """Simulador Post-Cuántico (PQC)."""
  print("\n[*] Módulo de Criptografía Poscuántica (PQC):")
  print("-" * 65)
  q_hash = hashlib.sha3_512(text.encode()).hexdigest()
  print(f"    [+] Hash Post-Cuántico (SHA3-512): {q_hash}")
  print("    [+] Resistencia frente a algoritmos de Shor y Grover.")
  print("-" * 65)


def main():
  parser = argparse.ArgumentParser(
      description="Crypstofus v3.0 - Suite Criptográfica de Grado Industrial"
  )
  parser.add_argument(
      "-t", "--text", required=False, help="Texto o datos de entrada"
  )
  parser.add_argument(
      "-m",
      "--mode",
      required=True,
      choices=["b64-enc", "b64-dec", "hex-enc", "hex-dec", "hash", "aes", "rsa", "ecc", "pqc"],
      help="Modo criptográfico industrial a ejecutar",
  )

  args = parser.parse_args()

  print("=================================================================")
  print("          CRYPTOFUS v3.0 - SUITE INDUSTRIAL & MODERNA           ")
  print("=================================================================")
  if args.text:
    print(f"[*] Entrada: {args.text}")
  print(f"[*] Modo   : {args.mode}")
  print("=" * 65)

  if args.mode in ["b64-enc", "b64-dec", "hex-enc", "hex-dec"]:
    if not args.text:
      print("[-] Error: Requiere texto (-t).")
      return
    print(f"[+] Resultado: {codify_operations(args.text, args.mode)}")
  elif args.mode == "hash":
    if not args.text:
      print("[-] Error: Requiere texto (-t).")
      return
    generate_hashes(args.text)
  elif args.mode == "aes":
    if not args.text:
      print("[-] Error: Requiere texto (-t) para cifrar con AES-GCM.")
      return
    aes_gcm_encrypt(args.text)
  elif args.mode == "rsa":
    if not args.text:
      print("[-] Error: Requiere texto (-t) para probar cifrado RSA.")
      return
    rsa_asymmetric_operations(args.text)
  elif args.mode == "ecc":
    elliptic_curve_crypto()
  elif args.mode == "pqc":
    if not args.text:
      args.text = "QuantumSeed2026"
    post_quantum_simulation(args.text)


if __name__ == "__main__":
  main()
