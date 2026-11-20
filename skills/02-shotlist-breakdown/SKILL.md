---
name: shotlist-breakdown
description: Use when breaking an approved 90-second historical-figure script into an 11-scene (8s each) shot list — narration text, start/end frame prompts, camera movement, continuity notes, and engagement-maximizing variation suggestions per scene. Second stage of the Type I pipeline.
---

# Shot-List / Desglose de Escenas

## Cuándo usar este skill

Después de aprobar el guion de `01-historytelling-design`, antes de generar keyframes.

## Input

```json
{
  "script_id": "string",
  "script_text": "string",
  "emotional_beat_map": []
}
```

## Parámetros fijos (decisiones congeladas del diseño)

- **Duración estándar: 90s → 11 escenas de 8s** (90 / 8 ≈ 11.25; la última escena puede ajustarse a ~6-8s para cerrar exacto en 90s).
- **Segmentación: 1 generación FLF2V de 8s por escena** (no se divide en 2 de 4s). LTX-2.5 soporta hasta 20s por generación en modo Fast, así que 8s está cómodamente dentro de rango.

## Proceso

1. Partir el guion en N escenas de 8s según el `emotional_beat_map`.
2. Para cada escena, generar:
   - `scene_id` (ej. `scene_01` … `scene_11`)
   - `narration_text` — línea de VO exacta para esa escena
   - `start_frame_prompt` / `end_frame_prompt` — descripción visual detallada (pose, iluminación, encuadre, vestuario)
   - `camera_movement` — lenguaje cinemático por defecto para esa escena
   - `continuity_notes` — el end-frame de la escena N debe enlazar visualmente con el start-frame de la escena N+1 (misma locación/ángulo aproximado si la transición es continua, o corte deliberado si no lo es)
3. **Generar `variant_suggestions`** por escena: 2-3 alternativas de `camera_movement`/pacing/encuadre pensadas para maximizar engagement (ej. push-in lento vs. pan lateral vs. corte estático). Reglas:
   - En escenas con el rostro del personaje en primer plano, **priorizar movimientos simples** (push-in lento, encuadre estático) — los movimientos grandes aumentan el riesgo de drift de identidad en la etapa FLF2V (ver nota de riesgo en `03-keyframe-generation` y `04-flf2v-runcomfy`).
   - Reservar movimientos más dramáticos para tomas amplias, de ambiente, o sin el rostro como foco principal.
4. Selección de variante: manual (tú) o vía heurística de scoring (ej. integración futura con vidIQ) — no bloqueante para continuar el pipeline; si no hay selección explícita, usar la variante por defecto marcada en el shot-list.

## Output

```json
{
  "script_id": "string",
  "scenes": [
    {
      "scene_id": "scene_01",
      "narration_text": "string",
      "start_frame_prompt": "string",
      "end_frame_prompt": "string",
      "camera_movement": "string — variante seleccionada",
      "variant_suggestions": [
        { "label": "push-in lento", "camera_movement": "string", "risk_level": "bajo" },
        { "label": "pan lateral", "camera_movement": "string", "risk_level": "medio" }
      ],
      "continuity_notes": "string",
      "duration_seconds": 8
    }
  ]
}
```

## Siguiente etapa

→ `03-keyframe-generation`
