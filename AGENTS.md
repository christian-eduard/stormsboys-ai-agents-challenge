# Reglas Para Agentes

Este workspace prepara una entrega competitiva para el Google for Startups AI Agents Challenge. Todo agente que trabaje aqui debe priorizar claridad, modularidad, trazabilidad y cumplimiento del reto.

## Direccion Actual

- Track principal: Track 3 - Refactor for Google Cloud Marketplace & Gemini Enterprise.
- Track secundario/evidencia: Track 2 - Optimize Existing Agents, usado para demostrar evaluacion, guardrails y mejora de fiabilidad.
- Producto real: plataforma de lectura interactiva donde usuarios, autores y editoriales suben libros; Gemini analiza la obra; y agentes de personajes, escenas, lugares, voz, publisher y admin hacen la experiencia operable.
- Don Quijote es el caso demo principal, no el producto completo.

## Principios

- Trabajar siempre dentro de `stormsboys-ai-agents-challenge`.
- No modificar ni depender de otros proyectos desde este workspace.
- Se puede leer la app original solo como referencia de producto cuando el usuario lo pida, pero no copiar deuda tecnica ni credenciales.
- No leer ni copiar secretos, `.env`, keystores, tokens o claves.
- No crear recursos en Google Cloud sin plan previo aprobado.
- Documentar antes de implementar cuando la decision afecte arquitectura, seguridad, costes o criterios del challenge.
- Preferir modulos pequenos con contratos claros.
- Mantener cada cambio ligado a un requisito del challenge o a la demo.

## Fuentes permitidas

- Guia oficial del challenge.
- Documentacion oficial de Google Cloud y Gemini.
- Documentacion generada dentro de este workspace.
- App original `Stormsboys_libros/libros-ia-app` solo como referencia conceptual y tecnica, nunca como fuente ciega de codigo.

## Prohibido

- Copiar configuraciones antiguas sin revisarlas.
- Arrastrar nombres legacy como `ElevenLabs` si realmente se usa Google TTS o Gemini.
- Hardcodear claves, URLs privadas o credenciales demo.
- Mezclar rutas `/api` y `/api/v1` sin decision documentada.
- Implementar agentes sin pruebas de evaluacion y trazas observables.
- Reducir el producto a una demo de un unico libro.
- Mezclar memoria canon y memoria ficcion.

## Flujo De Trabajo

1. Leer `README.md` y este archivo.
2. Leer `HANDOFF.md`.
3. Leer `docs/product/04-original-product-model.md`.
4. Leer `docs/track3/01-track3-marketplace-strategy.md`.
5. Revisar el documento de alcance correspondiente.
6. Si aparece una decision importante, crear o actualizar un ADR.
7. Implementar en modulos pequenos.
8. Agregar pruebas o checklist de validacion.
9. Actualizar documentacion si cambia comportamiento.

## Convenciones

- Idioma de documentacion: espanol.
- Codigo y nombres tecnicos: ingles cuando sea natural.
- Markdown simple, sin informacion sensible.
- Cada modulo debe explicar su responsabilidad en un README local si no es obvio.

## Definition Of Done

Un cambio se considera terminado cuando:

- Esta alineado con Track 3 o aporta evidencia Track 2 de calidad.
- No introduce deuda conocida de otros proyectos.
- Tiene documentacion minima.
- Tiene plan de validacion o prueba.
- No expone secretos.
- Puede explicarse en la demo de 1-2 minutos.
