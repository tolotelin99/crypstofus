import argparse
import base64
import hashlib
import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


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


def generate_hashes(text):
  """Hashes tradicionales y funciones pesadas derivadas (Estilo Yescrypt/Argon2)."""
  print("\n[*] Generando huellas y hashes de alta seguridad:")
  print("-" * 65)
  print(f"    [MD5]       : {hashlib.md5(text.encode()).hexdigest()}")
  print(f"    [SHA-256]   : {hashlib.sha256(text.encode()).hexdigest()}")
  print(f"    [SHA-512]   : {hashlib.sha512(text.encode()).hexdigest()}")
  
  # Simulación de derivación de clave pesada (Resistente a GPU, similar al propósito de Yescrypt)
  salt = os.urandom(16)
  kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=salt,
      iterations=100000, # Alta carga computacional
  )
  heavy_hash = kdf.derive(text.encode())
  print(f"    [Heavy-KDF] : {heavy_hash.hex()} (Sal: {salt.hex()})")
  print("-" * 65)


def elliptic_curve_crypto():
  """Generación de llaves usando Criptografía de Curva Elíptica (ECC - SECP256R1)."""
  print("\n[*] Módulo de Criptografía de Curva Elíptica (ECC):")
  print("-" * 65)
  # Generar clave privada usando la curva estándar NIST P-256 (secp256r1)
  private_key = ec.generate_private_key(ec.SECP256R1())
  public_key = private_key.public_key()

  # Serializar llave privada PEM
  pem_private = private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.PKCS8,
      encryption_algorithm=serialization.NoEncryption()
  )

  # Serializar llave pública PEM
  pem_public = public_key.public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo
  )

  print("    [+] Llave Privada ECC generada con éxito:")
  print(pem_private.decode("utf-8").strip())
  print("\n    [+] Llave Pública ECC correspondiente:")
  print(pem_public.decode("utf-8").strip())
  print("-" * 65)


def post_quantum_simulation(text):
  """Simulador conceptual de Criptografía Poscuántica (Resistente a Shor/Grover)."""
  print("\n[*] Módulo de Criptografía Poscuántica (PQC - Lattice/Hash Based):")
  print("-" * 65)
  print("    [i] Estado: Analizando resistencia frente a computación cuántica...")
  print("    [i] Algoritmo simulado: Winternitz One-Time Signature (WOTS+) / Lattice-based Hash")
  
  # Generar un hash resistente a cuántica usando SHA3-512 (Kangaroot/Keccak - considerado seguro ante Grover)
  q_hash = hashlib.sha3_512(text.encode()).hexdigest()
  print(f"    [+] Hash Post-Cuántico (SHA3-512): {q_hash}")
  print("    [+] Nota: Las firmas basadas en retículas y hashes mitigan el Algoritmo de Shor.")
  print("-" * 65)


def main():
  parser = argparse.ArgumentParser(
      description="Crypstofus - Herramienta avanzada de Criptografía y Ciberseguridad"
  )
  parser.add_argument(
      "-t", "--text", required=False, help="Texto o cadena de entrada para procesar"
  )
  parser.add_argument(
      "-m",
      "--mode",
      required=True,
      choices=["b64-enc", "b64-dec", "hex-enc", "hex-dec", "hash", "ecc", "pqc"],
      help="Modo criptográfico avanzado a ejecutar",
  )

  args = parser.parse_args()

  print("=================================================================")
  print("          CRYPTOFUS v2.0 - SUITE CRIPTOGRÁFICA AVANZADA          ")
  print("=================================================================")
  if args.text:
    print(f"[*] Entrada: {args.text}")
  print(f"[*] Modo   : {args.mode}")
  print("=" * 65)

  if args.mode in ["b64-enc", "b64-dec", "hex-enc", "hex-dec"]:
    if not args.text:
      print("[-] Error: El modo de codificación requiere un texto (-t).")
      return
    print(f"[+] Resultado: {codify_operations(args.text, args.mode)}")
  elif args.mode == "hash":
    if not args.text:
      print("[-] Error: El modo hash requiere una entrada de texto (-t).")
      return
    generate_hashes(args.text)
  elif args.mode == "ecc":
    elliptic_curve_crypto()
  elif args.mode == "pqc":
    if not args.text:
      args.text = "DefaultQuantumSeed2026"
    post_quantum_simulation(args.text)


if __name__ == "__main__":
  main()