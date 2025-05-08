# ✅ Tests de Modelos (`ModelTests`)

Este archivo contiene pruebas unitarias para verificar que los modelos del sistema funcionen correctamente. Las pruebas se ejecutan usando `django.test.TestCase`.

---

## ⚙️ Configuración Inicial (`setUp`)
Antes de cada test, se crean las siguientes instancias:
- Un usuario (`testuser`)
- Dos equipos (`Team One` y `Team Two`)
- Un juego (`Test Game`)
- Un torneo con fecha futura y 2 equipos permitidos (`Test Tournament`)

---

## 🧪 Pruebas Incluidas

### 🎮 `test_game_creation`
Verifica que el nombre del juego se representa correctamente como string.

### 🏷️ `test_team_creation`
Verifica que el nombre del equipo se representa correctamente como string.

### 👤 `test_player_creation`
Crea un jugador con MMR y asegura que:
- Está vinculado al equipo correcto.
- Su representación en string contiene el nombre del usuario.

### 🏆 `test_tournament_creation`
Verifica la creación y representación textual del torneo.

### 🚫 `test_tournament_team_unique`
Comprueba que no se puede registrar el mismo equipo dos veces en el mismo torneo (restricción `unique_together`).

### ⚔️ `test_match_creation`
Crea un partido entre dos equipos y verifica que su representación en string incluye "Partido".

### 🧾 `test_match_result_creation`
Crea un resultado de partido, verifica:
- El equipo ganador.
- Que su string incluye "Resultado:".

### 📜 `test_match_log_creation`
Crea un log de partido con un evento y verifica que dicho evento se representa correctamente.

### 🎁 `test_reward_creation`
Crea una recompensa y verifica su representación como `"Nombre (X coins)"`.

### 💸 `test_redemption_creation`
Verifica que el canje de una recompensa por parte de un usuario se representa como: `"username redeemed recompensa"`.

---

## 🧹 Limpieza (`tearDown`)
Después de cada test, se eliminan todas las instancias creadas para evitar interferencias entre pruebas.

---

## 📝 Notas
- Se usa `assertEqual` y `assertIn` para validar resultados esperados.
- La prueba de unicidad espera una `Exception`; podría ser más precisa usando `IntegrityError`.

---



## 🔄 Navegación
[⬅️ Volver al README principal](../README.md)
