---
name: keyframe-generation
description: Use when generating the start/end keyframe image pair for each scene of a Type I short, anchoring the historical figure's identity across all 11 scenes via InstantID + IPAdapter FaceID + ControlNet + FaceDetailer in ComfyUI/RunComfy, or accepting externally pre-generated images as a bypass. Third stage of the Type I pipeline.
---

# Generación de Keyframes (start/end frame)

## Cuándo usar este skill

Después de aprobar el shot-list de `02-shotlist-breakdown`, antes de renderizar video en `04-flf2v-runcomfy`.

## Input

```json
{
  "script_id": "string",
  "scenes": [ { "scene_id": "scene_01", "start_frame_prompt": "...", "end_frame_prompt": "..." } ],
  "reference_image": "path/url — retrato limpio de la figura histórica, una sola vez por short",
  "external_keyframes": "opcional — si se proveen, se usan directo y se salta la generación interna (ver 'Input alternativo' abajo)"
}
```

## Mecanismo de consistencia — default: InstantID (ComfyUI/RunComfy)

1. **Una sola imagen de referencia** por figura histórica (retrato limpio, rostro centrado, cuadrado idealmente) — generarla o seleccionarla una vez al inicio de esta etapa.
2. Grafo ComfyUI: `Load Reference Face → IPAdapter FaceID Plus v2 (+ CLIP-Vision, + FaceID LoRA) → ControlNet OpenPose (pose/encuadre por escena) → KSampler → FaceDetailer (repaso de rostro) → Upscale`.
3. Ajustes recomendados de partida: IPAdapter weight 0.6-0.8 (más bajo = domina el prompt y el rostro deriva; más alto = rostro fijo pero expresiones más rígidas), CFG 4-5 para evitar quemado con InstantID, resolución 1016×1016 o similar centrada en el sujeto.
4. Corre en la misma GPU de RunComfy ya rentada para FLF2V (etapa 4) — sin costo adicional por imagen, pero valida que el workflow de keyframes no compita por GPU-tiempo con el workflow de video si corren en la misma Deployment.
5. Generar 2 imágenes (start/end) por escena × 11 escenas = 22 imágenes por short, nombradas `{scene_id}_start.png` / `{scene_id}_end.png`.

## Input alternativo — bypass soportado

Esta etapa debe aceptar **imágenes ya generadas externamente** (ej. producidas con Nano Banana Pro / Gemini 3.1 Flash Image, u otro motor) en lugar de generarlas vía InstantID:

- Si llegan 2 imágenes por escena ya nombradas/trazables al `scene_id`, la etapa las usa directo y salta el grafo ComfyUI de esta etapa.
- Útil para: probar otro motor de imagen en un short puntual sin tocar el resto del pipeline, o resolver casos donde InstantID no logre buena fidelidad (ángulos extremos, expresiones difíciles para el adaptador).

## Riesgo residual a vigilar

Imágenes consistentes en los dos extremos de una escena **no garantizan** que el video FLF2V se mantenga consistente *dentro* del clip — los pipelines I2V pueden introducir drift de apariencia, especialmente con movimientos de cámara grandes. Este riesgo se mitiga parcialmente en `02-shotlist-breakdown` (preferir `camera_movement` simple en escenas con rostro en primer plano) y debe validarse explícitamente en el piloto de `04-flf2v-runcomfy`.

## Output

```json
{
  "script_id": "string",
  "reference_image_used": "path/url",
  "keyframes": [
    { "scene_id": "scene_01", "start_image": "path", "end_image": "path", "source": "instantid | external" }
  ]
}
```

## Siguiente etapa

→ `04-flf2v-runcomfy`
