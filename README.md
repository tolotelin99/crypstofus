# Crypstofus v10.0 🛡️🔐

**Crypstofus** es una suite criptográfica modular, portátil y de alto rendimiento diseñada con fines académicos y de auditoría de seguridad (UGR). Su enfoque principal es la eficiencia, un uso mínimo de recursos y la implementación de lógica autosuficiente sin dependencias pesadas de terceros.

## 🚀 Características Principales

* **Aritmética Modular & Criptografía Clásica/Moderna:** Módulos avanzados de RSA, Rabin-Miller, Curvas Elípticas (ECC) y cifrado híbrido AES-GCM + ChaCha20.
* **Infraestructura de Clave Pública (PKI):** Generación, validación y auditoría de certificados X.509 y flujos TLS.
* **Módulo de Hashing y Auditoría de Contraseñas (Estilo Hashcat / John):**
  * Cálculo de hashes SHA-256.
  * **Ataque por Diccionario Híbrido:** Soporta listas internas avanzadas (CrackStation/SecLists master top), lectura de archivos locales `.txt` y **Streaming Web directo** desde enlaces *Raw* de GitHub sin necesidad de descargar archivos locales.
  * **Ataque Algorítmico al Vuelo:** Generación matemática optimizada mediante `itertools` con rangos ampliados para PINs numéricos y patrones alfanuméricos.

## 📦 Instalación y Ejecución

Cloná el repositorio y ejecutá el script principal:

```bash
git clone [https://github.com/tolotelin99/crypstofus.git](https://github.com/tolotelin99/crypstofus.git)
cd crypstofus
python crypstofus.py
🛠️ Tecnologías Utilizadas
Python 3.x

Librerías nativas/estándar: cryptography, hashlib, itertools, urllib, os, time, string.
