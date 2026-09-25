# Crypstofus v3.0

**Crypstofus** es una suite criptográfica avanzada de grado industrial desarrollada en Python, diseñada para profesionales de la ciberseguridad, analistas y entusiastas del desarrollo seguro bajo la filosofía Unix (herramientas modulares, limpias y altamente especializadas).

---

##  Características Principales (v3.0)

- **Codificación Clásica**: Base64 (Codificación y Decodificación) y Hexadecimal.
- **Hashes y Derivación de Claves (KDF)**: MD5, SHA-256, SHA-512 y PBKDF2-HMAC-SHA256 (Heavy-KDF resistente a ataques masivos por fuerza bruta).
- **Cifrado Simétrico Moderno**: AES-256-GCM (proporciona confidencialidad e integridad autenticada de grado bancario/militar).
- **Cifrado Asimétrico Real**: RSA-2048 con relleno OAEP (Estándar de la industria).
- **Curvas Elípticas (ECC)**: Generación de pares de llaves asimétricas utilizando el estándar NIST P-256 (`secp256r1`) en formato PEM.
- **Criptografía Poscuántica (PQC)**: Simulación estructurada de resistencia frente a la amenaza de la computación cuántica (Algoritmos de Shor y Grover) mediante hashes SHA3-512.

---

##  Instalación

Clona el repositorio e instala la única dependencia moderna requerida (`cryptography`):

```bash
git clone [https://github.com/tolotelin99/crypstofus.git](https://github.com/tolotelin99/crypstofus.git)
cd crypstofus
pip install cryptography