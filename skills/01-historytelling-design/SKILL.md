---
name: historytelling-design
description: Use when generating the narrative script for a Faceless YC Type I short — selects among 3 narrative approaches (Hero's Journey, Redemption Arc, etc.), applies the CIBERTALES values-lesson model to a historical figure, and produces a timed 90-second script with an emotional beat map. First stage of the Type I pipeline.
---

# Historytelling Design

## Cuándo usar este skill

Cuando ya existe una figura histórica / temática aprobada (vía Creator-Market Fit / IKIGAI 2.0) y se necesita el guion narrativo de un short Tipo I antes de pasar al desglose de escenas.

## Input

```json
{
  "historical_figure": "string — nombre y período de la figura histórica",
  "target_duration_seconds": 90,
  "source_notes": "string opcional — hallazgos de investigación, ángulo de Creator-Market Fit, público objetivo"
}
```

## Proceso

1. **Investigación rápida** de la figura histórica: hechos verificables, contexto, tensión narrativa central, lección de valores aplicable.
2. **Generar 3 enfoques narrativos distintos** sobre el mismo hecho histórico (ej. Hero's Journey, Redemption Arc, Cautionary Tale — ajustar según lo que mejor sirva al hecho concreto). No reusar el mismo enfoque en shorts consecutivos del mismo lote sin justificación.
3. **Aplicar el modelo CIBERTALES**: cada enfoque debe entregar (a) admiración por la figura, (b) una lección de valores clara y aplicable a la vida del espectador, (c) sabiduría práctica — no solo biografía.
4. **Seleccionar el enfoque más convincente** de los 3 (criterio: fuerza del gancho inicial + claridad de la lección + autenticidad histórica).
5. **Redactar el guion** a 90 segundos, con pacing psicológico cronometrado (hook en los primeros 3-5s, desarrollo, climax, resolución/lección, CTA si aplica).
6. **Mapear beats emocionales** por bloque de tiempo, para que la etapa de shot-list pueda alinear cámara/ritmo a la emoción de cada momento.

## Output

```json
{
  "script_id": "string",
  "narrative_approach": "string — enfoque elegido",
  "approaches_considered": ["string", "string", "string"],
  "script_text": "string — guion completo, 90s",
  "emotional_beat_map": [
    { "time_range": "0-8s", "beat": "hook / intriga", "intensity": "alta" },
    { "time_range": "8-24s", "beat": "desarrollo / contexto", "intensity": "media" }
  ],
  "historical_accuracy_notes": "string — fuentes/afirmaciones a verificar en QA"
}
```

## Reutiliza

Tu framework de producción existente (guiones de 90s, 3 enfoques narrativos, modelo CIBERTALES) — este skill lo empaqueta como paso formal y reproducible, no lo reemplaza.

## Dependencias

Ninguna externa — skill de razonamiento/redacción puro. Consume el output de Creator-Market Fit (figura ya seleccionada).

## Siguiente etapa

→ `02-shotlist-breakdown`
