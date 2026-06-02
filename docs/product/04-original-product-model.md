# Modelo Real Del Producto

Este documento fija la interpretacion correcta de la aplicacion original que inspira el proyecto del challenge. No estamos creando solo una demo de chat con un libro. Estamos creando una plataforma de lectura interactiva donde cada libro se convierte en un sistema de agentes.

## Producto

Stormsboys Libros IA permite que un usuario, autor o editorial suba libros propios o libres de derechos. La plataforma analiza la obra, extrae su estructura narrativa y prepara agentes conversacionales basados en los personajes, lugares y escenas del libro.

El valor principal es que el lector no solo lee: puede conversar con el universo de la obra, escuchar respuestas, explorar escenas y, si el modo lo permite, crear lineas narrativas alternativas.

## Roles

### Lector

Puede:

- Registrarse e iniciar sesion.
- Explorar libros publicos.
- Leer libros disponibles.
- Guardar progreso.
- Marcar favoritos.
- Hablar con personajes.
- Hablar con lugares.
- Participar en escenas o grupos de personajes.
- Escuchar respuestas o narracion.

### Autor

Puede:

- Subir libros propios.
- Ver el analisis generado.
- Revisar personajes, lugares y escenas.
- Probar conversaciones.
- Publicar el libro para otros usuarios si corresponde.

### Publisher / Editorial

Puede:

- Subir libros de su catalogo.
- Gestionar disponibilidad para usuarios.
- Ver metricas de lectura, conversaciones y engagement.
- Entender que personajes o escenas generan mas interaccion.
- Preparar catalogos interactivos como producto B2B.

### Superadministrador

Puede:

- Gestionar usuarios.
- Cambiar roles.
- Gestionar libros y catalogos.
- Ver metricas globales.
- Auditar configuracion, uso y calidad.
- Operar la plataforma.

## Flujo Principal

1. El usuario sube un PDF o texto con metadatos basicos.
2. El backend extrae texto.
3. El libro queda en estado de procesamiento.
4. Gemini analiza el libro.
5. Se extraen personajes, lugares, escenas/capitulos y sinopsis.
6. Se calcula psicologia de personajes: personalidad, estilo de habla, rasgos OCEAN, deseos, miedos y contexto relacional.
7. Se divide el libro en chunks semanticos.
8. Se generan embeddings y se guardan en PostgreSQL + pgvector.
9. El libro queda disponible para lectura y conversacion.
10. El sistema genera metricas para lector, editorial y administracion.

## Idioma

La experiencia principal para el challenge y Devpost es ingles, porque la descripcion, el
video y la evaluacion de jueces deben entenderse sin friccion.

El producto tambien debe ofrecer espanol como idioma secundario funcional:

- La UI de demo debe permitir cambiar entre `English` y `Espanol`.
- Los endpoints conversacionales deben aceptar `language=en|es`.
- El Character Agent debe responder en el idioma seleccionado.
- El modo canon y el modo ficcion deben mantener la misma regla de idioma.
- La documentacion de producto puede estar en espanol para coordinacion interna, pero la
  submission publica debe estar en ingles.

Regla para agentes paralelos: no hardcodear textos solo en ingles dentro de flujos de usuario.
Si se anade una pantalla o endpoint conversacional, debe respetar el idioma seleccionado o
dejar documentado por que queda pendiente.

## Modos De Conversacion

### Modo Canon / Real

El personaje responde dentro del libro. La conversacion debe estar anclada en:

- Fragmentos recuperados por RAG.
- Perfil psicologico del personaje.
- Estado emocional.
- Historial de conversacion.
- Restricciones del canon.

En este modo el sistema debe evitar contradicciones. Si el usuario intenta cambiar hechos de la obra, el personaje puede reaccionar desde su psicologia, pero no debe convertir el cambio en canon.

### Modo Ficcion / Historia Alternativa

El personaje sigue partiendo de la obra, pero el usuario puede co-crear una rama narrativa alternativa.

Este modo debe:

- Mantener identidad y psicologia del personaje.
- Aceptar desviaciones creativas.
- Guardar la evolucion narrativa.
- Separar el historial de ficcion del historial canon.
- Crear material reutilizable como alternativa, escena derivada o futura obra.

La regla clave: ficcion no significa caos. Es una expansion controlada y trazable desde el canon.

## Experiencias

### Lector

Debe poder leer el libro con herramientas de lectura, voz y progreso.

### Personajes

Cada personaje debe comportarse como un agente con:

- Identidad.
- Memoria.
- Voz.
- Estado emocional.
- Restricciones de canon.
- Capacidad de evolucion ficcional cuando el modo lo permite.

### Lugares

Los lugares pueden responder como guias narrativos o entidades del mundo del libro, basados en fragmentos donde aparecen.

### Escenas

Las escenas permiten hablar dentro de un capitulo o momento narrativo concreto.

### Grupos

Los chats grupales permiten reunir varios personajes, mantener memoria compartida y producir respuestas diferenciadas por personaje.

## Don Quijote Como Caso Demo

Don Quijote debe usarse como libro demostrador porque:

- Es reconocible.
- Es de dominio publico.
- Tiene personajes muy diferenciados.
- Permite contrastar canon y ficcion de forma clara.
- El episodio de los molinos es perfecto para demostrar RAG, personalidad y modo alternativo.

Pero Don Quijote no es el producto. Es el caso de prueba principal.

## Implicacion Para El Challenge

La entrega debe mostrar una plataforma B2B/B2C operable:

- B2C: lectores interactuan con libros.
- B2B: editoriales convierten catalogos en experiencias interactivas y medibles.
- Admin: la plataforma se opera con control, seguridad y metricas.

Esto encaja principalmente con Track 3: refactorizar un agente/producto existente para Google Cloud Marketplace y Gemini Enterprise.
