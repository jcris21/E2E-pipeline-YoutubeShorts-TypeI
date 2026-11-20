"""
runcomfy_client.py
Cliente de referencia para llamar a una Deployment de RunComfy Serverless API
(ComfyUI Cloud) con el patrón de 'overrides' en vez de reenviar el grafo completo.

IMPORTANTE — dos cosas a verificar antes de usar esto en producción:

1. Los NODE_ID_* en build_overrides() son placeholders. Reemplázalos por los
   IDs reales de tu grafo una vez exportes el workflow_api.json real desde tu
   canvas de ComfyUI Cloud (ver workflows/README.md).
2. Las rutas de API (RUNCOMFY_API_BASE, /deployments/.../run, /jobs/{id}) y
   la forma de la respuesta (job_id, status, output_url) están escritas según
   el patrón general documentado de RunComfy Serverless API, pero no fueron
   verificadas contra la referencia de API más reciente de tu cuenta — revisa
   la documentación/dashboard de RunComfy para tu Deployment específica antes
   de correr esto, y ajusta rutas/campos si no coinciden.

Este script no incluye lógica de reintentos de producción — es un punto de
partida, no un cliente listo para producción sin pruebas.

Uso esperado (una llamada por escena, dentro del skill 04-flf2v-runcomfy):

    from runcomfy_client import render_scene

    result = render_scene(
        scene_id="scene_01",
        start_image_url="https://.../scene_01_start.png",
        end_image_url="https://.../scene_01_end.png",
        camera_movement="push-in lento, 35mm, luz dorada",
        duration_seconds=8,
    )
"""

import os
import time
import requests

RUNCOMFY_API_BASE = os.environ.get("RUNCOMFY_API_BASE", "https://api.runcomfy.net")
RUNCOMFY_API_KEY = os.environ.get("RUNCOMFY_API_KEY", "")
RUNCOMFY_DEPLOYMENT_ID = os.environ.get("RUNCOMFY_DEPLOYMENT_ID", "")

# --- Placeholders: reemplazar con los IDs reales del grafo exportado ---
NODE_ID_FIRST_FRAME = "<NODE_ID_first_frame_loader>"
NODE_ID_LAST_FRAME = "<NODE_ID_last_frame_loader>"
NODE_ID_PROMPT_TEXT = "<NODE_ID_prompt_text>"
NODE_ID_DURATION = "<NODE_ID_duration_or_length>"


def build_overrides(start_image_url: str, end_image_url: str, camera_movement: str, duration_seconds: int) -> dict:
    """Construye el objeto 'overrides' esperado por la Deployment."""
    return {
        "overrides": {
            NODE_ID_FIRST_FRAME: {"inputs": {"image": start_image_url}},
            NODE_ID_LAST_FRAME: {"inputs": {"image": end_image_url}},
            NODE_ID_PROMPT_TEXT: {"inputs": {"text": camera_movement}},
            NODE_ID_DURATION: {"inputs": {"duration_seconds": duration_seconds}},
        }
    }


def render_scene(
    scene_id: str,
    start_image_url: str,
    end_image_url: str,
    camera_movement: str,
    duration_seconds: int = 8,
    poll_interval_s: int = 5,
    timeout_s: int = 600,
) -> dict:
    """
    Dispara el render de una escena en la Deployment de LTX-2.5 FLF2V y
    hace polling hasta completar. Devuelve dict con scene_id, video_url,
    render_time_seconds — usar para alimentar el log de piloto descrito
    en skills/04-flf2v-runcomfy/SKILL.md.
    """
    if not RUNCOMFY_API_KEY or not RUNCOMFY_DEPLOYMENT_ID:
        raise RuntimeError(
            "Faltan RUNCOMFY_API_KEY / RUNCOMFY_DEPLOYMENT_ID en el entorno."
        )

    payload = build_overrides(start_image_url, end_image_url, camera_movement, duration_seconds)
    headers = {"Authorization": f"Bearer {RUNCOMFY_API_KEY}", "Content-Type": "application/json"}

    t0 = time.time()
    submit_url = f"{RUNCOMFY_API_BASE}/deployments/{RUNCOMFY_DEPLOYMENT_ID}/run"
    resp = requests.post(submit_url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    job = resp.json()
    job_id = job.get("job_id") or job.get("id")

    status_url = f"{RUNCOMFY_API_BASE}/jobs/{job_id}"
    while True:
        if time.time() - t0 > timeout_s:
            raise TimeoutError(f"Timeout esperando render de {scene_id} (job {job_id})")
        status_resp = requests.get(status_url, headers=headers, timeout=30)
        status_resp.raise_for_status()
        status = status_resp.json()
        if status.get("status") == "completed":
            return {
                "scene_id": scene_id,
                "video_url": status.get("output_url"),
                "render_time_seconds": round(time.time() - t0, 1),
            }
        if status.get("status") == "failed":
            raise RuntimeError(f"Render falló para {scene_id}: {status.get('error')}")
        time.sleep(poll_interval_s)


if __name__ == "__main__":
    # Ejemplo de smoke test manual — ajustar paths/URLs reales antes de correr.
    result = render_scene(
        scene_id="scene_01",
        start_image_url="https://example.com/scene_01_start.png",
        end_image_url="https://example.com/scene_01_end.png",
        camera_movement="push-in lento, 35mm, luz dorada",
        duration_seconds=8,
    )
    print(result)
