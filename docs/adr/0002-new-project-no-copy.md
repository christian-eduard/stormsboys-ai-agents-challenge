# ADR 0002: Proyecto Nuevo Sin Mezclar Otros Proyectos

## Estado

Aceptada.

## Contexto

Existen proyectos previos con valor funcional, pero tambien pueden contener deuda tecnica, configuraciones antiguas, nombres legacy, posibles secretos y rutas inconsistentes.

## Decision

Crear un proyecto nuevo dentro de esta raiz, autocontenido, sin copiar codigo ni configuracion de otros proyectos.

## Consecuencias

- Se reduce riesgo de arrastrar errores.
- Se requiere implementar de nuevo solo lo necesario.
- Cada modulo nuevo debe justificar su inclusion.
- La documentacion manda sobre la improvisacion.
