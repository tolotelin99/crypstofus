# Crypstofus v10.0 🛡️🔐

**Crypstofus** es una suite criptográfica modular, portátil y de alto rendimiento diseñada con fines académicos y de auditoría de seguridad (UGR). Su enfoque principal es la eficiencia, un uso mínimo de recursos y la implementación de lógica autosuficiente sin dependencias pesadas de terceros.

## 🚀 Características Principales

* **Aritmética Modular & Criptografía Clásica/Moderna:** Módulos avanzados de RSA, Rabin-Miller, Curvas Elípticas (ECC) y cifrado híbrido AES-GCM + ChaCha20.
* **Infraestructura de Clave Pública (PKI):** Generación, validación y auditoría de certificados X.509 y flujos TLS.
* **Módulo de Hashing y Auditoría de Contraseñas (Estilo Hashcat / John):**
  * Cálculo de hashes SHA-256.
  * **Ataque por Diccionario Híbrido:** Soporta listas internas avanzadas (CrackStation/SecLists master top), lectura de archivos locales `.txt` y **Streaming Web directo** desde enlaces *Raw* de GitHub sin necesidad de descargar archivos locales.
  * **Ataque Algorítmico al Vuelo:** Generación matemática optimizada mediante `itertools` con rangos ampliados para PINs numéricos y patrones alfanuméricos.

## 📋 Módulos Disponibles en la Suite

1. **Aritmética Modular** -> Generar Primos (Rabin-Miller)
2. **Diffie-Hellman** -> Intercambio Seguro de Claves
3. **Cifrado Híbrido** -> Encriptar (RSA + AES-GCM)
4. **Descifrado Híbrido** -> Desencriptar JSON
5. **KDF Pesado** -> Proteger contraseñas (Argon2)
6. **Cifrar ChaCha20** -> Cifrado Simétrico Móvil
7. **Descifrar ChaCha20** -> Recuperar Mensaje Simétrico
8. **Hashes Rápidos** -> SHA3 / BLAKE2 (Integridad)
9. **Generar Llaves ECC** -> Asimétrico Moderno (NIST P-256)
10. **Firmar Mensaje** -> Crear Firma Digital (ECDSA)
11. **Verificar Firma** -> Validar Autenticidad (ECDSA)
12. **Generar Certificado** -> Identidad Digital (X.509 TLS)
13. **Analizar Certificado** -> Forense de X.509
14. **Auditar Navegadores** -> Compatibilidad Chrome/Firefox/Tor
15. **Utilidades Bytes** -> Conversión ASCII/Hex/Binario
16. **Cifrados Clásicos** -> Cifrado César y Criptoanálisis
17. **Generador Primos** -> Listar Primos para RSA
18. **PLOT Curva Elíptica** -> Visualizador Gráfico (ECC)
19. **Hashing & Auditar** -> SHA-256 & Fuerza Bruta de Contraseñas
20. **Salir**

## 📦 Instalación y Ejecución

Cloná el repositorio y ejecutá el script principal:

```bash
git clone [https://github.com/tolotelin99/crypstofus.git](https://github.com/tolotelin99/crypstofus.git)
cd crypstofus
python crypstofus.py
🛠️ Tecnologías Utilizadas
Python 3.x

Librerías nativas/estándar: cryptography, hashlib, itertools, urllib, os, time, string.
