---
name: voiceover-tts
description: Use when generating the voice-over track for a Type I short's narration text via Fish Audio's s2.1-pro-free model and a fixed catalog voice reference_id, through the community Fish Audio MCP server. Fifth stage of the Type I pipeline — runs independently of the video stage.
---

# Narración / Voz en Off (TTS)

## Cuándo usar este skill

En paralelo a `04-flf2v-runcomfy` (no depende de los clips de video) — solo necesita el `narration_text` por escena del shot-list de `02-shotlist-breakdown`.

## Input

```json
{
  "script_id": "string",
  "scenes": [ { "scene_id": "scene_01", "narration_text": "string" } ],
  "voice_reference_id": "string fijo — voz de catálogo elegida para el canal, consistente a través de los 100 shorts"
}
```

## Herramienta elegida (decisión congelada)

- **Fish Audio**, modelo **`s2.1-pro-free`** (misma calidad que S2.1 Pro, sin costo, sin tope duro de uso documentado a la fecha de este diseño — revalidar periódicamente que el tier gratuito siga vigente).
- **Voz de catálogo** (no clonada) — un `reference_id` fijo para todo el canal, para mantener identidad sonora consistente entre shorts.
- Integración vía el **MCP server de comunidad** (`fish-audio-mcp-server` / `@alanse/fish-audio-mcp-server`): tool `fish_audio_tts(text, reference_id)`, sin infraestructura propia que mantener.
- Ver `scripts/fish_audio_client.py` para una implementación de referencia fuera de un entorno MCP (ej. para llamarlo directo desde un nodo HTTP Request de n8n).

## Proceso

1. Concatenar o procesar por separado el `narration_text` de cada escena (recomendado: una llamada TTS por escena para poder re-sincronizar fácilmente si una escena cambia de duración).
2. Generar audio con `model: "s2.1-pro-free"`, `reference_id: voice_reference_id` fijo.
3. Normalizar duración: si el audio generado no calza con los 8s de la escena, ajustar ritmo de narración en el guion/shot-list en vez de estirar/comprimir el audio artificialmente (preserva calidad natural de voz).
4. Entregar la pista de VO por escena, lista para que `06-assembly-hyperframes` la sincronice con el clip de video correspondiente.

## Output

```json
{
  "script_id": "string",
  "voiceover_clips": [
    { "scene_id": "scene_01", "audio_file": "path — {scene_id}_vo.mp3", "duration_seconds": "number" }
  ]
}
```

## Costo estimado

Lote completo de 100 shorts (90s c/u) ≈ 135,000 caracteres de narración. Con `s2.1-pro-free`: **~$0**. Con el tier de pago S2.1 Pro ($15/M bytes UTF-8) como respaldo si el free tier cambia de términos: **~$2-3 para todo el lote**.

## Siguiente etapa

→ `06-assembly-hyperframes`
