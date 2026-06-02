# ADR 0003: Cloud Run Primero

## Estado

Aceptada.

## Contexto

El challenge acepta despliegues en Google Cloud. Para una demo rapida, Cloud Run ofrece menor complejidad que GKE y encaja bien con frontend/backend contenerizados.

## Decision

Usar Cloud Run como runtime principal para la entrega inicial.

## Consecuencias

- Menor complejidad operativa.
- Mejor velocidad para llegar a demo.
- GKE queda fuera del alcance inicial.
- El backend debe ser stateless y externalizar datos en Cloud SQL/Storage.
