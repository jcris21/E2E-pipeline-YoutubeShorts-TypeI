"""
fish_audio_client.py
Cliente de referencia para generar voz en off vía Fish Audio (modelo
s2.1-pro-free, voz de catálogo fija) fuera de un entorno MCP — útil para
un nodo HTTP Request de n8n o para correr el skill 05-voiceover-tts como
script standalone.

Si el entorno de ejecución ya tiene disponible el MCP server de comunidad
(fish-audio-mcp-server / @alanse/fish-audio-mcp-server), preferir ese tool
(fish_audio_tts(text, reference_id)) sobre este script — es la ruta ya
probada y con menos piezas propias que mantener. Este archivo es el
respaldo directo-a-API para contextos sin MCP (ej. un nodo Code/HTTP en n8n).

NOTA: la ruta de endpoint (/v1/tts) y la forma del payload de este script
son una aproximación razonable al patrón estándar de Fish Audio, pero no
fueron verificadas línea por línea contra docs.fish.audio — Fish Audio
también publica un SDK oficial de Python (ver docs.fish.audio/sdk-reference/python)
que es más seguro de usar que reconstruir las llamadas HTTP a mano. Verifica
el endpoint y los campos exactos en la documentación antes de producción.

Uso esperado (una llamada por escena, dentro del skill 05-voiceover-tts):

    from fish_audio_client import generate_voiceover

    result = generate_voiceover(
        scene_id="scene_01",
        text="En 1813, Bolívar cruzó los Andes...",
        reference_id=os.environ["FISH_VOICE_REFERENCE_ID"],
        output_path="scene_01_vo.mp3",
    )
"""

import os
import requests

FISH_API_BASE = os.environ.get("FISH_API_BASE", "https://api.fish.audio")
FISH_API_KEY = os.environ.get("FISH_API_KEY", "")
FISH_MODEL = os.environ.get("FISH_MODEL", "s2.1-pro-free")


def generate_voiceover(scene_id: str, text: str, reference_id: str, output_path: str) -> dict:
    """
    Genera audio TTS para una escena y lo guarda en output_path.
    Devuelve dict con scene_id, output_path, bytes_written.
    """
    if not FISH_API_KEY:
        raise RuntimeError("Falta FISH_API_KEY en el entorno.")
    if len(text.encode("utf-8")) > 10000:
        raise ValueError(
            f"narration_text de {scene_id} excede 10,000 caracteres — "
            "límite documentado por llamada del MCP server de Fish Audio."
        )

    payload = {
        "text": text,
        "reference_id": reference_id,
        "model": FISH_MODEL,
        "format": "mp3",
    }
    headers = {"Authorization": f"Bearer {FISH_API_KEY}", "Content-Type": "application/json"}

    resp = requests.post(f"{FISH_API_BASE}/v1/tts", json=payload, headers=headers, timeout=60)
    resp.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(resp.content)

    return {
        "scene_id": scene_id,
        "output_path": output_path,
        "bytes_written": len(resp.content),
    }


def generate_voiceover_batch(scenes: list, reference_id: str, output_dir: str) -> list:
    """
    scenes: lista de dicts { "scene_id": str, "narration_text": str }
    Devuelve lista de resultados de generate_voiceover(), uno por escena.
    """
    os.makedirs(output_dir, exist_ok=True)
    results = []
    for scene in scenes:
        output_path = os.path.join(output_dir, f"{scene['scene_id']}_vo.mp3")
        results.append(
            generate_voiceover(
                scene_id=scene["scene_id"],
                text=scene["narration_text"],
                reference_id=reference_id,
                output_path=output_path,
            )
        )
    return results


if __name__ == "__main__":
    # Smoke test manual — ajustar texto/reference_id reales antes de correr.
    result = generate_voiceover(
        scene_id="scene_01",
        text="Texto de prueba para validar la integración con Fish Audio.",
        reference_id=os.environ.get("FISH_VOICE_REFERENCE_ID", "<reference_id de catálogo>"),
        output_path="scene_01_vo.mp3",
    )
    print(result)
