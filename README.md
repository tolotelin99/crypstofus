# Crypstofus v7.0 - Suite Criptográfica Industrial

**Crypstofus** es una suite criptográfica interactiva y avanzada desarrollada en Python. Diseñada para profesionales de la ciberseguridad, fusiona la matemática pura (aritmética modular) con los estándares modernos de cifrado de grado industrial en una única interfaz unificada.

---

## 🚀 Características Principales (v7.0)

La suite cuenta con 8 módulos interactivos:

1. **Aritmética Modular (Rabin-Miller)**: Generación de números primos seguros de gran tamaño (ej. 2048 bits) eludiendo la ineficiencia de la fuerza bruta pura.
2. **Diffie-Hellman (Merkle)**: Simulación de intercambio seguro de claves matemáticas sobre redes públicas sin transmitir el secreto.
3. **Cifrado Híbrido (AES-GCM + RSA-OAEP)**: Encriptación de archivos unificando la velocidad de AES de 256 bits con el blindaje asimétrico de claves RSA.
4. **Descifrado Híbrido**: Verificación de integridad (vía etiquetas de autenticación Galois) y apertura de cofres JSON.
5. **KDF Pesado (Argon2 / PBKDF2)**: Derivación de claves diseñada para consumir RAM/CPU y resistir ataques masivos de fuerza bruta por GPU y algoritmos de Grover.
6. **Cifrado Simétrico Móvil (ChaCha20-Poly1305)**: Implementación del algoritmo AEAD ultrarrápido preferido en conexiones HTTPS móviles modernas.
7. **Hashes de Integridad (SHA3 / BLAKE2)**: Funciones de resumen criptográfico de última generación para verificación de descargas y blockchains.
8. **Asimétrico Moderno (ECC)**: Generación de pares de claves de Curvas Elípticas (NIST P-256) en formato PEM.

---

## 🛠️ Instalación y Uso

Clona el repositorio e instala la única dependencia moderna requerida (`cryptography`):

```bash
git clone [https://github.com/tolotelin99/crypstofus.git](https://github.com/tolotelin99/crypstofus.git)
cd crypstofus
pip install cryptography
python crypstofus.py

