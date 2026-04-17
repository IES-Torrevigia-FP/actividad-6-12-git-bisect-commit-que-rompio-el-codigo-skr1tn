# Reflexión – Actividad 6.12: `git bisect`

## 1. ¿Cómo funciona `git bisect` y qué problema resuelve?

`git bisect` es una herramienta de Git que permite encontrar automáticamente
el commit que introdujo un bug, usando búsqueda binaria sobre el historial
de commits.

El problema que resuelve es el siguiente: cuando un proyecto tiene muchos
commits y en algún momento aparece un error, revisar uno a uno todos los
commits sería muy lento. Con `git bisect`, en lugar de revisar todos,
Git divide el rango de commits a la mitad en cada paso. Si tienes
100 commits sospechosos, solo necesitas unos 7 pasos (log2(100)) para
encontrar el commit culpable.

El proceso es:
1. Indicar un commit donde el bug está presente (BAD).
2. Indicar un commit donde el bug no existía (GOOD).
3. Git hace checkout del commit intermedio.
4. Compruebas si el bug está presente y marcas el commit como good o bad.
5. Repites hasta que Git identifica el primer commit malo.

## 2. Situación real donde `git bisect` sería especialmente útil

Imagina que estás trabajando en un videojuego con un equipo de
desarrolladores. El juego funciona bien en la versión 1.0 pero en la
versión 1.5 los jugadores reportan que el personaje atraviesa las paredes.
Entre esas dos versiones hay 200 commits de diferentes desarrolladores.

Con `git bisect` podrías:
- Marcar la v1.0 como GOOD (colisiones funcionan).
- Marcar la v1.5 como BAD (colisiones rotas).
- Ejecutar el juego en cada commit intermedio para comprobar la colisión.
- En unos 8 pasos, Git te indica exactamente qué commit rompió las colisiones.

Esto es mucho más eficiente que revisar 200 commits manualmente.

## 3. Requisitos previos para que `git bisect` sea eficaz

Para que `git bisect` funcione correctamente, el proyecto debe cumplir:

- **Commits atómicos y funcionales**: cada commit debe dejar el proyecto
  en un estado que se pueda compilar y ejecutar. Si hay commits intermedios
  que no compilan, git bisect no puede probarlos.

- **Prueba reproducible**: necesitas una forma clara y objetiva de
  determinar si un commit es good o bad. Lo ideal es tener un test
  automático (como test_contador.sh en esta actividad) que devuelva
  código de salida 0 si es correcto y no-0 si hay bug.

- **Conocer un commit good anterior**: debes saber en qué punto del
  historial el código funcionaba correctamente. Si no tienes esta
  referencia, no puedes iniciar el bisect.

- **Historial lineal o claro**: los merges y ramas complejas pueden
  complicar el proceso, aunque git bisect lo maneja razonablemente bien.

- **Bug reproducible**: el bug debe aparecer de forma consistente,
  no aleatoriamente. Los bugs intermitentes son muy difíciles de
  localizar con bisect.
