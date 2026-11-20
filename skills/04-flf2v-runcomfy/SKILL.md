---
name: flf2v-runcomfy
description: Use when rendering a scene's video clip from its start/end keyframe pair via RunComfy's Serverless API running LTX-2.5 FLF2V on an L40S (X-Large Plus) GPU deployment — calls the deployed endpoint with per-scene overrides instead of resending the full ComfyUI graph. Fourth stage of the Type I pipeline — the video engine.
---

# FLF2V — RunComfy / LTX-2.5 / L40S

## Cuándo usar este skill

Después de tener los keyframes de `03-keyframe-generation` para todas las escenas del short.

## Input

```json
{
  "scene_id": "string",
  "start_image": "path/url",
  "end_image": "path/url",
  "camera_movement": "string — prompt de movimiento de la escena, de 02-shotlist-breakdown",
  "duration_seconds": 8
}
```

## Infraestructura (ruta congelada del diseño)

- **RunComfy Serverless API (ComfyUI Cloud)**, workflow LTX-2.5 FLF2V.
- Deployment sobre GPU **X-Large Plus (L40S, 48GB)** — $2.99/hr Pay-as-you-go / $2.15/hr Pro.
- El workflow se exporta **una sola vez** como `workflow_api.json` (build/test en ComfyUI Cloud → Export API → Cloud Save → Deploy como Deployment).
- Cada llamada posterior usa el objeto `overrides` sobre esa Deployment — **no se reenvía el grafo completo por escena**.

⚠️ **El archivo `workflows/ltx25_flf2v_workflow_api.json` en este export es una plantilla/esqueleto, no el grafo real.** El JSON exacto (IDs de nodo, `class_type`, versión de los custom nodes de LTX-2.5 instalados) solo existe después de que tú armes y exportes el workflow desde tu propio canvas de ComfyUI Cloud en RunComfy — no se puede generar por fuera de ese entorno sin inventar valores. Ver `workflows/README.md`.

## Proceso

1. (Una sola vez) Construir el grafo LTX-2.5 FLF2V en ComfyUI Cloud, probarlo manualmente, exportar como `workflow_api.json`, Cloud Save, desplegar como Deployment.
2. Por cada escena: llamar al endpoint de la Deployment con `overrides` apuntando a `first_frame`, `last_frame`, `prompt` (camera_movement) y `duration`.
3. Desactivar audio nativo de LTX-2.5 si el modelo lo genera — el VO se añade por separado en `05-voiceover-tts`.
4. Guardar el clip resultante nombrado `{scene_id}.mp4`, sin audio.

## Pendiente de validar con piloto

No hay benchmark publicado de throughput GPU-segundo por segundo de video final específicamente en L40S para LTX-2.5. **Antes de proyectar el costo del lote completo de 100 shorts, correr 5-10 escenas de prueba** y medir:
- Tiempo real de generación por escena de 8s.
- Costo real por escena (tiempo × $2.99/hr o $2.15/hr).
- **Drift de identidad/apariencia dentro del clip** (no solo que los keyframes coincidan) — especialmente en escenas con `camera_movement` complejo. Si aparece drift notorio, volver a `02-shotlist-breakdown` y forzar variantes de movimiento más simples en esas escenas.

## Output

```json
{
  "scene_id": "string",
  "video_clip": "path — {scene_id}.mp4, sin audio",
  "render_time_seconds": "number — medir en el piloto",
  "gpu_cost_usd": "number — medir en el piloto"
}
```

## Siguiente etapa

→ `05-voiceover-tts` (en paralelo) → `06-assembly-hyperframes`
