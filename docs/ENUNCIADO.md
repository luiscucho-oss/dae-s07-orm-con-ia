# ORM con IA — duelo y verificador

Repositorio del laboratorio **extra de la semana 7** de Desarrollo de Aplicaciones
Empresariales (DAE). Un blog con autores, artículos, categorías, etiquetas y comentarios sobre
el que se escriben ocho consultas del ORM de Django, se comparan con las que escribe una IA y
se aprende a verificar lo que un modelo produce.

La guía del laboratorio (con su rúbrica) está en el campus virtual; aquí está el código.

## Puesta en marcha

```bash
python -m venv .venv
.venv\Scripts\activate          # en Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_blog      # carga los datos fijos: 4 autores, 15 artículos, 23 comentarios
```

`seed_blog` se puede repetir cuando quieras: borra los datos del blog y los vuelve a cargar
**siempre iguales**. Eso es lo que permite saber de antemano cuál es la respuesta correcta de
cada pregunta.

## Parte 1 — El duelo

Escribe tus ocho consultas en `blog/duel/team.py` (una función por pregunta) y compruébalas:

```bash
python manage.py duel                  # tus ocho respuestas
python manage.py duel --question q4    # solo una
python manage.py duel --source ai      # las respuestas de un asistente de IA a las mismas preguntas
```

Para cada pregunta el duelo dice si la respuesta es **correcta** (devuelve lo esperado con las
consultas que cabe esperar), **correcta pero cara** (el resultado es bueno y gasta muchas
consultas), **distinta** (devuelve otra cosa) o da **error**. Compara las tuyas con las de la IA
y decide cuáles aceptarías.

Para consultar el SQL de una respuesta mientras la depuras, usa la consola:

```bash
python manage.py shell
>>> from blog.duel import team
>>> print(team.q1().query)
```

## Parte 2 — Del rojo al verde

```bash
python manage.py test blog.tests.test_front_page
```

La prueba `test_front_page_runs_two_queries` **falla a propósito**: la portada funciona, pero
dispara una consulta por cada autor y por cada conjunto de etiquetas. Arréglala en
`blog/queries.py` hasta que pase. Para medir antes y después:

```bash
python manage.py runserver     # y abre http://127.0.0.1:8000/
```

## Parte 3 — La frontera

`blog/agent/registry.py` es una lista **cerrada** de acciones que un modelo puede pedir. Nada de
`eval`, nada de SQL libre. Pruébala con intenciones escritas a mano:

```bash
python manage.py agent --intent '{"action": "posts_per_author", "args": {}}'
python manage.py agent --intent '{"action": "comments_of_post", "args": {"post_id": 1}}'
python manage.py agent --intent '{"action": "delete_comments_of_post", "args": {"post_id": 1}}'
python manage.py agent --intent '{"action": "run_sql", "args": {}}'
```

Lee con atención los comentarios del artículo 1: uno de ellos intenta darle órdenes a un modelo.

## Todas las pruebas

```bash
python manage.py test
```

Una sola debe fallar mientras no hayas hecho la Parte 2.

## Estructura

| Ruta | Para qué |
|---|---|
| `blog/models.py` | `Author`, `Profile` (uno a uno), `Category`, `Tag`, `Post`, `Comment` |
| `blog/seed_data.py` | Los datos fijos, en Python puro |
| `blog/duel/team.py` | **Tus** ocho respuestas |
| `blog/duel/ai_answers.py` | Las de la IA, tal como las escribió |
| `blog/duel/questions.py` | Las preguntas y la respuesta esperada de cada una |
| `blog/queries.py` | La consulta de la portada (Parte 2) |
| `blog/agent/` | La pasarela de acciones (Parte 3) y un adaptador opcional a un modelo local |

## Convenciones del curso

Código, nombres y comentarios en inglés; explicaciones y entregables en español. PEP 8.
