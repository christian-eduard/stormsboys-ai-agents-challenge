# Control De Costes

## Objetivo

Usar los creditos de Google Cloud de forma prudente durante el challenge.

## Principios

- Preferir Cloud Run por escalado a cero.
- Usar instancias pequenas para demo.
- Evitar GKE en fase inicial.
- Apagar o pausar recursos no usados.
- Registrar recursos creados.

## Recursos Con Coste

- Cloud SQL.
- Cloud Run si recibe trafico.
- Cloud Storage.
- Gemini API.
- Logs de alto volumen.

## Reglas

- No crear recursos sin coste estimado.
- No dejar jobs infinitos.
- No subir libros grandes innecesarios.
- No ejecutar evaluaciones masivas sin limite de prompts.

## Checklist Diario

- Revisar Cloud Billing.
- Revisar Cloud Run revisions activas.
- Revisar Cloud SQL.
- Revisar Storage.
- Revisar cuotas Gemini.

## Politica Para Demo

La demo debe usar:

- Dataset pequeno.
- Libro demo controlado.
- Prompts predefinidos.
- Limite de tokens.
- Cache cuando tenga sentido.
