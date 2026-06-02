# Reglas Para Agentes

Este workspace prepara una entrega competitiva para el Google for Startups AI Agents Challenge. Todo agente que trabaje aqui debe priorizar claridad, modularidad, trazabilidad y cumplimiento del reto.

## Principios

- Trabajar siempre dentro de `stormsboys-ai-agents-challenge`.
- No modificar ni depender de otros proyectos desde este workspace.
- No leer ni copiar secretos, `.env`, keystores, tokens o claves.
- No crear recursos en Google Cloud sin plan previo aprobado.
- Documentar antes de implementar cuando la decision afecte arquitectura, seguridad, costes o criterios del challenge.
- Preferir modulos pequenos con contratos claros.
- Mantener cada cambio ligado a un requisito del challenge o a la demo.

## Fuentes permitidas

- Guia oficial del challenge.
- Documentacion oficial de Google Cloud y Gemini.
- Documentacion generada dentro de este workspace.

## Prohibido

- Copiar configuraciones antiguas sin revisarlas.
- Arrastrar nombres legacy como `ElevenLabs` si realmente se usa Google TTS o Gemini.
- Hardcodear claves, URLs privadas o credenciales demo.
- Mezclar rutas `/api` y `/api/v1` sin decision documentada.
- Implementar agentes sin pruebas de evaluacion y trazas observables.

## Flujo De Trabajo

1. Leer `README.md` y este archivo.
2. Revisar el documento de alcance correspondiente.
3. Si aparece una decision importante, crear o actualizar un ADR.
4. Implementar en modulos pequenos.
5. Agregar pruebas o checklist de validacion.
6. Actualizar documentacion si cambia comportamiento.

## Convenciones

- Idioma de documentacion: espanol.
- Codigo y nombres tecnicos: ingles cuando sea natural.
- Markdown simple, sin informacion sensible.
- Cada modulo debe explicar su responsabilidad en un README local si no es obvio.

## Definition Of Done

Un cambio se considera terminado cuando:

- Esta alineado con Track 2.
- No introduce deuda conocida de otros proyectos.
- Tiene documentacion minima.
- Tiene plan de validacion o prueba.
- No expone secretos.
- Puede explicarse en la demo de 1-2 minutos.
