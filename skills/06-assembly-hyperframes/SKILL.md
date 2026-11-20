---
name: assembly-hyperframes
description: Use when assembling a Type I short's final MP4 from its ordered video clips, VO track, captions and brand overlays via HyperFrames' /general-video HTML template and per-short variable overrides. Sixth stage of the Type I pipeline.
---

# Ensamblaje (HyperFrames)

## Cuándo usar este skill

Una vez estén listos todos los clips de `04-flf2v-runcomfy` y toda la pista de VO de `05-voiceover-tts` para un short.

## Input

```json
{
  "script_id": "string",
  "video_clips": [ { "scene_id": "scene_01", "video_clip": "path" } ],
  "voiceover_clips": [ { "scene_id": "scene_01", "audio_file": "path" } ],
  "background_music": "path opcional",
  "captions": "generadas por HyperFrames desde el audio, o .srt provisto"
}
```

## Herramienta elegida (decisión congelada)

**HyperFrames** (HeyGen, open-source Apache 2.0) — framework HTML→video: la composición se describe en una plantilla HTML (clips `<video>` con `data-start`/`data-duration`/`data-track-index`, pista de VO/música como `<audio>`, captions, overlays de marca) y se renderiza de forma determinística vía captura de frames + FFmpeg.

- **Plantilla base: `/general-video`** (catch-all multi-escena) — **no** `/faceless-explainer` (pensado para formato explicador/talking-head, no para narrativa cinemática multi-escena generada por IA).
- Corre en **CPU** vía CLI (`npx hyperframes render`) — no compite por GPU con la etapa de RunComfy.
- Requiere **Node.js 22+ y FFmpeg** en el entorno de ejecución (ej. paso independiente en n8n, o un contenedor ligero separado del GPU runner).
- Patrón: **una plantilla HTML fija por canal** + overrides de variables (rutas a clips/audio) por short — consistente con el patrón "template + overrides" del resto del pipeline.
- ⚠️ El framework gestiona el ciclo de vida de los clips por sí mismo — **no** llamar `video.play()`/`pause()` ni montar/desmontar clips manualmente; describir estructura y timing en el HTML y dejar que HyperFrames sincronice.

Ver `scripts/hyperframes/template_general_video.html` — plantilla de partida a validar/ajustar con `npx hyperframes init` y `npx hyperframes preview` antes de producción en volumen.

## Proceso

1. `npx hyperframes init` (una sola vez) para scaffolding del proyecto con el template `/general-video`.
2. Ajustar la plantilla HTML: 11 slots de `<video>` en orden de `scene_id`, una pista `<audio>` continua para el VO, pista opcional de música de fondo, zona de captions, overlay de marca/branding.
3. Por cada short: generar el archivo de overrides (rutas a los 11 clips + VO + música) y correr `npx hyperframes render` con esos overrides.
4. `npx hyperframes preview` para QA visual rápido antes del render final si hay dudas de sincronización.

## Output

```json
{
  "script_id": "string",
  "final_video": "path — MP4 final vertical 9:16, ~90s",
  "render_log": "string"
}
```

## Siguiente etapa

→ `07-qa-checklist`
