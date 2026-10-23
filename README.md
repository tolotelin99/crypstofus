# Crypstofus v10.0 🛡️🔐

**Crypstofus** es una suite criptográfica modular, portátil y de alto rendimiento diseñada con fines académicos y de auditoría de seguridad (UGR). Su arquitectura prioriza la eficiencia algorítmica, un consumo mínimo de recursos en entornos Windows y una implementación robusta basada en primitivas criptográficas estándar sin dependencias innecesarias.

---

## 🚀 Arquitectura y Características Técnicas de los Módulos

* **Módulos de Aritmética Modular y Primos (1 y 17):** Implementación de pruebas de primalidad probabilísticas mediante el test de *Rabin-Miller* y algoritmos optimizados de cribado para la generación segura de números primos requeridos en esquemas de clave asimétrica.
* **Protocolo Diffie-Hellman e Intercambio de Claves (Módulo 2):** Establecimiento seguro de secretos compartidos sobre canales no seguros mediante aritmética de grupos cíclicos discretos.
* **Cifrado Híbrido Asimétrico/Simétrico (Módulos 3 y 4):** Mecanismo de encapsulado de claves combinando *RSA* para el intercambio seguro del secreto y *AES-GCM* (Galois/Counter Mode) para la confidencialidad y autenticación de cargas útiles serializadas en JSON.
* **Derivación de Claves (KDF) y Cifrado de Flujo (Módulos 5, 6 y 7):** Integración de funciones de derivación robustas resistentes a ataques de fuerza bruta (*Argon2*) y cifrado simétrico de alta velocidad optimizado para entornos móviles o de recursos acotados mediante *ChaCha20*.
* **Integridad, Criptografía Asimétrica y Firmas (Módulos 8, 9, 10 y 11):** Funciones hash de alta velocidad para integridad (*SHA3* y *BLAKE2*), generación de pares de claves asimétricas basadas en curvas elípticas (*NIST P-256 / ECC*), y emisión/verificación de firmas digitales mediante *ECDSA*.
* **Infraestructura de Clave Pública (PKI) y Forense (Módulos 12, 13, 14 y 18):** Generación de identidades digitales y certificados autofirmados (*X.509 TLS*), análisis forense detallado de campos de certificados, herramientas de auditoría de compatibilidad de cifrado para navegadores (*Chrome, Firefox, Tor*) y un visualizador gráfico interactivo para la geometría de curvas elípticas.
* **Ingeniería de Bytes y Criptoanálisis Clásico (Módulos 15 y 16):** Utilidades de conversión e inspección de estructuras binarias, hexadecimales y ASCII, junto con herramientas analíticas para cifrados de sustitución histórica como el cifrado *César*.
* **Motor de Hashing y Auditoría de Contraseñas (Módulo 19 - Estilo Hashcat / John):**
  * **Cálculo de Hashes:** Generación de resúmenes criptográficos *SHA-256*.
  * **Ataque por Diccionario Híbrido:** Soporte avanzado para listas internas preconfiguradas (CrackStation / SecLists), carga de archivos locales `.txt` y **Streaming Web optimizado** que procesa archivos directamente desde enlaces *Raw* de GitHub renglón por renglón en memoria RAM, evitando descargas innecesarias al disco.
  * **Ataque Algorítmico al Vuelo:** Generación combinatoria matemática en tiempo real mediante `itertools` con rangos de búsqueda ampliados para PINs numéricos y patrones alfanuméricos complejos.

---

## 📋 Índice de Opciones del Menú

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

---

## 📦 Instalación y Ejecución

Cloná el repositorio, instalá las dependencias necesarias y ejecutá el script principal:

```bash
git clone [https://github.com/tolotelin99/crypstofus.git](https://github.com/tolotelin99/crypstofus.git)
cd crypstofus
pip install -r requirements.txt
python crypstofus.py
🛠️ Stack Tecnológico
Lenguaje: Python 3.x

Librerías Nativas y Estándar: hashlib, itertools, urllib, os, time, string

Librería Criptográfica Externa: cryptography
