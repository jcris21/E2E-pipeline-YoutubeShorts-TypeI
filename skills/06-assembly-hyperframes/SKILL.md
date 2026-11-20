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

Ver `scripts/hyperframes/template_general_video.html` — plantilla **validada con un render real** (ver `test-run-ada-lovelace.md`, sección "Validación real — etapa 6"). No es solo un boceto: se corrió efectivamente en sandbox con `hyperframes@0.9.71` (Node 22, FFmpeg) usando 11 clips + VO + música placeholder, y produjo un MP4 de 90.000s, 1080×1920, H.264/AAC.

## Reglas críticas descubiertas al validar (no estaban en la documentación previa)

- **Todo `<video>`/`<audio>` con `data-start` necesita un `id` único.** Sin él, `hyperframes render` **congela el video** y **silencia el audio** en el output final — sin error visible salvo que corras `npm run check` antes de renderizar (lo marca como `media_missing_id`, severidad error). Nunca saltar el `check` antes de `render`.
- **Elementos visuales con tiempo necesitan `class="clip"`** además de `id` — si no, `lint` avisa (warning) y Studio no puede editarlos como timeline target.
- **Un video sin audio propio** (como los clips mudos de LTX-2.5 FLF2V, cuya voz viene de la pista de VO separada) va con `data-has-audio="false"` + atributo `muted`. Un video que sí trae su propio audio (no es el caso aquí) usa `data-has-audio="true"` sin `muted`.
- **Overlays que no ocupan el frame completo** (ej. marca de agua/branding) no deben heredar `height:100%`/`width:100%` de `.clip` sin sobreescribirlo — si no, aparecen fuera de canvas (`canvas_overflow`) aunque el `top/left/bottom` parezca correcto.
- El checklist obligatorio del propio proyecto HyperFrames (`CLAUDE.md` que genera `init`) es: `npm run check` (lint + runtime + layout + motion + contraste) **antes** de `npm run render`, siempre — no es opcional ni solo para QA visual.

## Proceso

1. `npx hyperframes init <nombre> --example blank --resolution portrait --non-interactive --skip-skills` (una sola vez por proyecto/canal) para el scaffolding real.
2. Ajustar `index.html`: 11 `<video id="scene-NN" class="clip" ...>` en orden de `scene_id` con `data-start` acumulativo (0, 8, 16, ..., 80) y `data-duration` (8s, última escena 10s), `data-has-audio="false"` + `muted`; una pista `<audio id="voiceover-track">` continua para el VO; pista opcional `<audio id="music-track">` de música; overlay de marca como `<div>` con `id`, tamaño explícito (no heredar `.clip` sin ajustar) y, si se posiciona cerca de un borde, `data-layout-allow-safe-zone`.
3. Registrar el timeline vacío requerido por el runtime: `window.__timelines["<composition-id>"] = gsap.timeline({ paused: true })`.
4. Por cada short: inyectar las rutas reales (11 clips + VO + música) en la plantilla y correr `npm run check` — **debe pasar con 0 errores** antes de continuar.
5. `npm run render` (o `npx hyperframes render`) para el MP4 final. En este sandbox un short de 90s tardó ~6 min (screenshot/software GPU capture — en un runner con GPU de verdad o `chrome-headless-shell` debería ser más rápido).
6. `npx hyperframes preview` para QA visual interactivo si hace falta ajustar timing antes del render final (ver sección siguiente — **validado en vivo**, no solo documentado).

## Preview en vivo / edición interactiva (HyperFrames Studio) — validado

`npx hyperframes preview` levanta **Studio**, un servidor local (por defecto `http://localhost:3002`) con una UI de navegador para ver la composición renderizándose en vivo y editar elementos directamente — sin volver a correr `render` para cada ajuste.

**Esto se probó de extremo a extremo**, no solo se documentó:
- Dos lanzadores de un clic están en `scripts/hyperframes/`: `abrir-studio.cmd` (Windows) y `abrir-studio.sh` (macOS/Linux) — copian el patrón `cd "<carpeta del proyecto>" && npx --yes hyperframes@0.9.71 preview --port 3002`. Requieren Node.js 22+ instalado en esa máquina.
- Con Studio corriendo, se abrió `http://localhost:3002/#project/<nombre-del-proyecto>` en un navegador — la URL incluye `#project/<id>` para apuntar directo al proyecto si hay varios activos.
- Confirmado visualmente: el panel **Preview** reproduce la composición completa (clips, overlay de marca, timeline de 1:30 para un short de 90s); el panel **Timeline** lista las pistas; el panel **Layers/Inspector** permite seleccionar cualquier elemento por su `id` (de ahí la regla de IDs únicos arriba) y editarlo sin tocar el HTML a mano.
- ⚠️ Studio corre como proceso local — si la terminal/consola donde se lanzó se cierra, el servidor se cae. No es algo que un pipeline headless (n8n, CI) pueda usar: es una herramienta de **revisión humana** antes del render final de producción, no parte del flujo automatizado de etapas 1-8.

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
