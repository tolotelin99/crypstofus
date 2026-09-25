import argparse
import base64
import hashlib


def codify_operations(text, mode):
  """Maneja operaciones de codificación y decodificación clásica (Base64, Hex)."""
  try:
    if mode == "b64-enc":
      return base64.b64encode(text.encode("utf-8")).decode("utf-8")
    elif mode == "b64-dec":
      return base64.b64decode(text.encode("utf-8")).decode(
          "utf-8", errors="ignore"
      )
    elif mode == "hex-enc":
      return text.encode("utf-8").hex()
    elif mode == "hex-dec":
      return bytes.fromhex(text).decode("utf-8", errors="ignore")
  except Exception as e:
    return f"Error en operación de codificación: {e}"


def caesar_cipher(text, decrypt=False):
  """Cifrado y descifrado César clásico."""
  result = []
  shift = 13 if decrypt else 3  # Por defecto ROT13 si es inverso o César clásico
  for char in text:
    if char.isalpha():
      ascii_offset = ord("A") if char.isupper() else ord("a")
      if decrypt:
        res = chr((ord(char) - ascii_offset - 3) % 26 + ascii_offset)
      else:
        res = chr((ord(char) - ascii_offset + 3) % 26 + ascii_offset)
      result.append(res)
    else:
      result.append(char)
  return "".join(result)


def generate_hashes(text):
  """Genera hashes criptográficos comunes (MD5, SHA-256, SHA-512)."""
  print("\n[*] Generando huellas criptográficas (Hashes):")
  print("-" * 50)
  print(f"    [MD5]    : {hashlib.md5(text.encode()).hexdigest()}")
  print(f"    [SHA-256]: {hashlib.sha256(text.encode()).hexdigest()}")
  print(f"    [SHA-512]: {hashlib.sha512(text.encode()).hexdigest()}")
  print("-" * 50)


def main():
  parser = argparse.ArgumentParser(
      description=(
          "Crypstofus - Herramienta avanzada de Criptografía y Codificación"
      )
  )
  parser.add_argument(
      "-t",
      "--text",
      required=True,
      help="Texto o cadena de entrada para procesar",
  )
  parser.add_argument(
      "-m",
      "--mode",
      required=True,
      choices=["b64-enc", "b64-dec", "hex-enc", "hex-dec", "caesar", "hash"],
      help="Modo criptográfico a ejecutar",
  )

  args = parser.parse_args()

  print("==================================================")
  print("        CRYPTOFUS v1.0 - CORE CRIPTOGRÁFICO       ")
  print("==================================================")
  print(f"[*] Entrada: {args.text}")
  print(f"[*] Modo   : {args.mode}")
  print("=" * 50)

  if args.mode in ["b64-enc", "b64-dec", "hex-enc", "hex-dec"]:
    print(
        f"[+] Resultado Codificación/Decodificación:"
        f" {codify_operations(args.text, args.mode)}"
    )
  elif args.mode == "caesar":
    print(f"[+] Resultado César (Desplazamiento 3): {caesar_cipher(args.text)}")
  elif args.mode == "hash":
    generate_hashes(args.text)


if __name__ == "__main__":
  main()