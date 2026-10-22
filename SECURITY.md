# Políticas de Seguridad de Crypstofus

## Versiones Soportadas

Actualmente, solo la versión más reciente recibe parches de seguridad y actualizaciones de algoritmos y estándares criptográficos.

| Versión | Soportada          |
| ------- | ------------------ |
| v10.0.x | :white_check_mark: |
| < v9.0  | :x:                |

## Principios Criptográficos Aplicados en v10.0

Crypstofus implementa estrictamente las siguientes defensas modernas:

*   **Entropía Verdadera:** Sustitución de generadores débiles por `secrets` (CSPRNG) para nonces, sales y parámetros aleatorios.
*   **Mitigación de Oráculos:** RSA utiliza exclusivamente el esquema de relleno OAEP con MGF1 y SHA-256.
*   **Integridad Autenticada (AEAD):** Algoritmos simétricos (AES-GCM y ChaCha20-Poly1305) para prevenir la manipulación del texto cifrado.
*   **Resistencia a Fuerza Bruta:** Uso del estándar Argon2id recomendado por NIST para KDFs de contraseñas.
*   **Estándares Modernos de Identidad y Navegadores:** Soporte completo de Curvas Elípticas (NIST P-256), firmas ECDSA, parsing X.509 (TLS) y validación cruzada para motores de Chromium, Firefox y Tor.

## Reporte de Vulnerabilidades

Si descubrís una vulnerabilidad, por favor no crees un Issue público. Enviá un reporte detallado al administrador del repositorio.
