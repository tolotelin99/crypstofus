# Políticas de Seguridad de Crypstofus

## Versiones Soportadas

Actualmente, solo la versión más reciente recibe parches de seguridad y actualizaciones de algoritmos.

| Versión | Soportada          |
| ------- | ------------------ |
| v7.0.x  | :white_check_mark: |
| < v6.0  | :x:                |

## Principios Criptográficos Aplicados

En la versión 7.0, Crypstofus implementa estrictamente las siguientes defensas:

*   **Entropía Verdadera:** Sustitución de la librería `random` por `secrets` (CSPRNG) para toda generación de claves, nonces y sales (salts), previniendo ataques de predicción.
*   **Mitigación de Padding Oracles:** RSA utiliza exclusivamente el esquema de relleno OAEP con MGF1 y SHA-256.
*   **Integridad Autenticada (AEAD):** Todos los cifrados simétricos (AES y ChaCha20) implementan autenticación de mensajes por hardware/software (GCM y Poly1305) para prevenir la manipulación del texto cifrado (Ciphertext Malleability).
*   **Resistencia a Fuerza Bruta:** Uso del estándar Argon2id (recomendado por NIST) para la protección de contraseñas.

## Reporte de Vulnerabilidades

Si descubrís una vulnerabilidad, por favor no crees un Issue público. Enviá un reporte detallado al administrador del repositorio.
