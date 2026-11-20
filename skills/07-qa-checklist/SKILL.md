---
name: qa-checklist
description: Use when reviewing an assembled Type I short against the production checklist — VO/video sync, scene-to-scene continuity, identity-drift check, historical accuracy, values-message clarity, artifact/glitch check, and duration — before it moves to export. Seventh stage of the Type I pipeline.
---

# QA / Checklist de Revisión

## Cuándo usar este skill

Después de `06-assembly-hyperframes`, antes de `08-export-publish`.

## Input

```json
{
  "script_id": "string",
  "final_video": "path",
  "historical_accuracy_notes": "de 01-historytelling-design"
}
```

## Checklist (contra tu tabla "production checklists" en Airtable)

- [ ] **Sync VO/video** — la narración coincide temporalmente con la escena correspondiente en todas las 11 escenas.
- [ ] **Continuidad entre escenas** — las transiciones respetan los `continuity_notes` del shot-list; no hay saltos visuales abruptos no intencionados.
- [ ] **Consistencia de identidad del personaje** — revisar específicamente las escenas marcadas con `camera_movement` complejo (riesgo de drift dentro del clip FLF2V, no solo entre keyframes). Si hay drift notorio, regenerar esa escena con movimiento más simple antes de aprobar.
- [ ] **Precisión histórica** — validar contra `historical_accuracy_notes` de la etapa 1.
- [ ] **Claridad del mensaje de valores (CIBERTALES)** — la lección es reconocible y aplicable, no solo biografía.
- [ ] **Ausencia de artefactos/glitches** — revisar especialmente manos, fondos y transiciones de escena generadas por LTX-2.5.
- [ ] **Duración correcta** — ~90s, dentro de spec de YouTube Shorts.
- [ ] **Captions** — legibles, bien sincronizados, sin errores de transcripción del VO.

## Output

```json
{
  "script_id": "string",
  "status": "aprobado | rechazado",
  "notes": "string — hallazgos y qué etapa regenerar si fue rechazado"
}
```

## Si es rechazado

Volver a la etapa específica que causó el problema (no reiniciar todo el pipeline): drift de identidad → `03-keyframe-generation` o `04-flf2v-runcomfy`; sync de audio → `05-voiceover-tts` o `06-assembly-hyperframes`; precisión histórica → `01-historytelling-design`.

## Siguiente etapa

→ `08-export-publish` (si aprobado)
