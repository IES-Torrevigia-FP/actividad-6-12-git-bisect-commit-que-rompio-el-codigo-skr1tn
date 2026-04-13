# 🎯 Actividad 6.12 – `git bisect`: encontrar el commit que rompió el código

> Sabes usar `log`, `revert`, `reset` y `blame` para inspeccionar y deshacer cambios.
> En esta actividad aprenderás a usar **`git bisect` para localizar automáticamente el commit que introdujo un bug**, usando búsqueda binaria sobre el historial.

---

## 🎯 Objetivos de la actividad

Al finalizar esta actividad serás capaz de:

- Explicar qué hace `git bisect` y qué necesita para funcionar (un commit “good” y uno “bad”).
- Usar `git bisect` de forma manual (`good` / `bad`) para encontrar un commit con bug.
- Finalizar la búsqueda con `git bisect reset`.
- Entender la idea de integrar un test/manual de verificación en el proceso.

---

## 🧠 Conceptos clave: cómo funciona `git bisect`

- `git bisect` usa **búsqueda binaria** sobre el historial de commits para encontrar el que introdujo un bug.
- Necesitas:
  - Un commit **bad**: donde el bug está presente (normalmente `HEAD`).
  - Un commit **good**: anterior, donde sabes que el bug no existía.
- Git va saltando a la mitad del rango, tú ejecutas una prueba (manual o automática) y le dices si ese commit es `good` o `bad`.
- Tras varios pasos, te devuelve el **primer commit donde apareció el bug**.

---

## 🧩 Parte 1 – Preparar un historial con un bug introducido en mitad

### Reto 1.1 – Crear el repositorio y varios commits

1. Crea una carpeta para esta actividad:

   ```bash
   mkdir actividad-6-12-git-bisect
   cd actividad-6-12-git-bisect
   ```

2. Inicializa el repositorio:

   ```bash
   git init
   ```

3. Crea `contador.py` (o `.js` si prefieres) con un comportamiento correcto:

   ```python
   # contador.py
   # Versión inicial correcta

   def siguiente(n):
       return n + 1

   if __name__ == "__main__":
       import sys
       valor = int(sys.argv) [docs.github](https://docs.github.com/en/education/manage-coursework-with-github-classroom/teach-with-github-classroom/create-an-assignment-from-a-template-repository)
       print(siguiente(valor))
   ```

4. Añade y haz commit:

   ```bash
   git add contador.py
   git commit -m "Versión inicial correcta de contador"
   ```

5. Crea varios commits “intermedios”:
   - Commit 2:

     ```bash
     echo "# Log: añadido comentario 1" >> contador.py
     git add contador.py
     git commit -m "Añade comentario 1"
     ```

   - Commit 3:

     ```bash
     echo "# Log: añadido comentario 2" >> contador.py
     git add contador.py
     git commit -m "Añade comentario 2"
     ```

6. Introduce un bug en la función:

   ```python
   def siguiente(n):
       return n + 2 # BUG intencionado: debería ser +1
   ```

7. Commit del bug:

   ```bash
   git add contador.py
   git commit -m "Introduce bug en siguiente (suma 2)"
   ```

8. Añade aún algún commit más después del bug para hacer el historial más largo:

   ```bash
   echo "# Log: añadido comentario 3" >> contador.py
   git add contador.py
   git commit -m "Añade comentario 3"
   ```

9. Comprueba el historial:

   ```bash
   git log --oneline
   ```

### Checkpoint 1 – Evidencia

- Crea `cp1-historial-bisect.txt` con la salida de `git log --oneline`.

---

## 🧩 Parte 2 – Preparar una prueba simple “good/bad”

### Reto 2.1 – Definir cómo sabrás si un commit está bien o mal

Para `git bisect` necesitas una forma de saber si en un commit el programa está correcto (good) o contiene el bug (bad).

En este ejercicio usarás una prueba manual sencilla:

- Buen comportamiento esperado: `python contador.py 5` debe imprimir `6`.
- Comportamiento con bug: imprimirá `7`.

1. Prueba con el commit actual (HEAD):

   ```bash
   python contador.py 5
   ```

   Si ya estás después del bug, verás `7` → **BAD**.

2. Anota: “test manual: `python contador.py 5` → 6 = good, 7 = bad”.

### Checkpoint 2 – Evidencia

- Crea `cp2-prueba-manual.txt` con:
  - El comando de prueba y el resultado actual.
  - Una explicación de cómo decides si un commit es `good` o `bad`.

---

## 🧩 Parte 3 – Ejecutar `git bisect` de forma manual

### Reto 3.1 – Iniciar el bisect con un good y un bad

1. Asegúrate de estar en la rama donde hiciste los commits (por defecto, `main`):

   ```bash
   git status
   ```

2. Inicia el modo bisect:

   ```bash
   git bisect start
   ```

3. Marca el commit actual (HEAD), donde sabes que el bug existe, como **bad**:

   ```bash
   git bisect bad
   ```

4. Localiza en el log un commit que sepas que era correcto (por ejemplo, el primero o segundo commit, antes de tocar `siguiente`):

   ```bash
   git log --oneline
   ```

5. Marca ese commit como **good**:

   ```bash
   git bisect good <hash_commit_bueno>
   ```

   Ahora Git seleccionará automáticamente un commit intermedio y hará checkout de él.

### Reto 3.2 – Probar commits intermedios

1. Para cada commit que Git te muestre (se irá moviendo en cada paso):
   - Ejecuta:

     ```bash
     python contador.py 5
     ```

   - Si el resultado es `6`, marca el commit como good:

     ```bash
     git bisect good
     ```

   - Si el resultado es `7`, marca el commit como bad:

     ```bash
     git bisect bad
     ```

2. Git repetirá el proceso (búsqueda binaria) hasta encontrar el primer commit donde aparece el bug.

3. Al final, verás un mensaje tipo:

   ```text
   <hash> is the first bad commit
   ```

### Reto 3.3 – Salir de bisect

1. Cuando hayas encontrado el commit, sal del modo bisect:

   ```bash
   git bisect reset
   ```

   Esto te devolverá al estado original (normalmente HEAD).

### Checkpoint 3 – Evidencia

- Crea `cp3-proceso-bisect.txt` con:
  - El commit marcado como good (hash y mensaje).
  - El commit marcado como bad inicial (hash y mensaje).
  - El hash y mensaje del commit que `git bisect` ha identificado como “first bad commit”.

---

## 🧩 Parte 4 – (Opcional) Automatizar con un script

> Esta parte es opcional pero muy interesante.

### Reto 4.1 – Usar `git bisect run`

`git bisect run` permite automatizar las pruebas usando un script o comando cuyo código de salida indica good (0) o bad (≠0).

1. Crea un script sencillo `test_contador.sh` (en Linux/macOS; en Windows puedes usar un `.bat` equivalente):

   ```bash
   #!/bin/bash
   python contador.py 5 | grep -qx "6"
   ```

   - Si el resultado es 6, `grep` devolverá 0 → good.
   - Si es otro valor, devolverá código distinto de 0 → bad.

2. Dale permisos de ejecución:

   ```bash
   chmod +x test_contador.sh
   ```

3. Inicia de nuevo un bisect (puedes repetir todo el escenario o crear uno nuevo):

   ```bash
   git bisect start
   git bisect bad # commit actual
   git bisect good <hash_commit_bueno>
   ```

4. Ejecuta:

   ```bash
   git bisect run ./test_contador.sh
   ```

   Git irá ejecutando el script en varios commits y marcándolos automáticamente como good/bad según el código de salida.

5. Al terminar, mostrará el commit culpable. No olvides:

   ```bash
   git bisect reset
   ```

### Checkpoint 4 – Evidencia (opcional)

- Crea `cp4-bisect-run.txt` con:
  - El contenido de `test_contador.sh`.
  - El resultado final mostrado por `git bisect run`.

---

## 🧩 Parte 5 – Reflexión final

Crea `reflexion-6-12.md` y responde:

1. Explica con tus palabras cómo funciona `git bisect` y qué problema resuelve.
2. Describe una situación real en un proyecto donde `git bisect` sería especialmente útil (por ejemplo, bugs que aparecen después de muchos commits).
3. ¿Qué requisitos previos debe cumplir el proyecto para que `git bisect` sea eficaz (tests reproducibles, saber qué es “buggy” y qué no, etc.)?

---

## 📦 Entrega esperada en el repositorio

Tu repositorio de la Actividad 6.12 debe incluir:

- `contador.py`
- `test_contador.sh` (si realizas la parte opcional).
- `cp1-historial-bisect.txt`
- `cp2-prueba-manual.txt`
- `cp3-proceso-bisect.txt`
- `cp4-bisect-run.txt` (si realizas la parte opcional)
- `reflexion-6-12.md`

---

## 🏁 Evaluación sugerida

- 4 pts – Uso correcto de `git bisect` manual (`start`, `good`, `bad`, `reset`) para localizar un commit con bug.
- 3 pts – (Opcional) Uso de `git bisect run` con un script de prueba.
- 3 pts – Calidad de la reflexión en `reflexion-6-12.md` (comprender el enfoque sistemático de depuración).

**Puntuación máxima: 10 puntos.**

---

## 🤖 Evaluación automática y redacción de informe

Esta actividad incluye una evaluación automática similar a la de la actividad 6.9, adaptada a `git bisect` (proceso manual `good/bad`, `reset` y parte opcional con `git bisect run`):

- Workflow: `.github/workflows/evaluacion.yml`
- Script de evaluación: `tools/evaluar_repo.py`
- Script de redacción IA: `tools/ai_redactor.py`

### ¿Qué genera?

Al ejecutarse en GitHub Actions, se generan los siguientes archivos en `reportes/`:

- `informe.md` (resumen técnico de evaluación)
- `informe.json` (métricas en formato estructurado)
- `metricas.csv` (puntuaciones por criterio)
- `arbol.txt` (resumen del árbol del repositorio)

Si hay credenciales de IA configuradas en Secrets/Variables, también se generan:

- `retro.md` (retroalimentación redactada por IA)
- `retro.docx` (versión formal en Word)

### Parámetros del workflow (`workflow_dispatch`)

- `min_commits` (por defecto: `5`)
- `required_files` (por defecto: `contador.py,cp1-historial-bisect.txt,cp2-prueba-manual.txt,cp3-proceso-bisect.txt,reflexion-6-12.md`)

---
