"""
airtable_sync.py
Cliente de referencia para crear/actualizar el registro de un short Tipo I
en tu base Airtable de 9 tablas (videos, scripts, visual assets, audio
assets, performance metrics, expenses, research sources, production
checklists, values library) — usado por el skill 08-export-publish.

IMPORTANTE:
1. Ya usas el conector MCP de Airtable para gestión de base de datos con
   relaciones de campo complejas y enlace de tablas — si ese conector o el
   nodo nativo de Airtable de n8n están disponibles en tu entorno de
   ejecución, prefiérelos sobre este script. Este archivo es el respaldo
   para un contexto sin esos conectores (ej. un script standalone).
2. Los nombres de campo usados abajo (ej. "Script", "Historical Figure",
   "Video File") son placeholders razonables, no los nombres reales de tu
   base — ajústalos a tu schema real antes de usar esto. Esta base no fue
   leída campo por campo para este export; solo se conocen los nombres de
   las 9 tablas.

Requiere: pip install pyairtable
"""

import os
from pyairtable import Api

AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY", "")
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "")

TABLE_VIDEOS = "videos"
TABLE_SCRIPTS = "scripts"
TABLE_VISUAL_ASSETS = "visual assets"
TABLE_AUDIO_ASSETS = "audio assets"
TABLE_PRODUCTION_CHECKLISTS = "production checklists"


def _table(name: str):
    api = Api(AIRTABLE_API_KEY)
    return api.table(AIRTABLE_BASE_ID, name)


def sync_short_record(
    script_id: str,
    historical_figure: str,
    script_text: str,
    video_file_path: str,
    voiceover_file_path: str,
    qa_status: str,
    title: str,
    description: str,
) -> dict:
    """
    Crea registros enlazados en scripts / visual assets / audio assets /
    production checklists, y el registro principal en videos enlazando a
    los tres. Devuelve el record_id de 'videos'.

    AJUSTAR nombres de campo (claves de los dicts "fields") a tu schema real
    antes de usar esto en producción — ver nota al inicio del archivo.
    """
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        raise RuntimeError("Faltan AIRTABLE_API_KEY / AIRTABLE_BASE_ID en el entorno.")

    scripts_table = _table(TABLE_SCRIPTS)
    script_record = scripts_table.create(
        {
            "Script ID": script_id,
            "Historical Figure": historical_figure,
            "Script Text": script_text,
        }
    )

    visual_assets_table = _table(TABLE_VISUAL_ASSETS)
    visual_record = visual_assets_table.create(
        {
            "Script ID": script_id,
            "Video File": video_file_path,
        }
    )

    audio_assets_table = _table(TABLE_AUDIO_ASSETS)
    audio_record = audio_assets_table.create(
        {
            "Script ID": script_id,
            "Voiceover File": voiceover_file_path,
        }
    )

    checklist_table = _table(TABLE_PRODUCTION_CHECKLISTS)
    checklist_record = checklist_table.create(
        {
            "Script ID": script_id,
            "Status": qa_status,
        }
    )

    videos_table = _table(TABLE_VIDEOS)
    video_record = videos_table.create(
        {
            "Script ID": script_id,
            "Title": title,
            "Description": description,
            "Linked Script": [script_record["id"]],
            "Linked Visual Asset": [visual_record["id"]],
            "Linked Audio Asset": [audio_record["id"]],
            "Linked Checklist": [checklist_record["id"]],
        }
    )

    return {"videos_record_id": video_record["id"]}


if __name__ == "__main__":
    # Smoke test manual — ajustar valores reales y nombres de campo antes de correr.
    result = sync_short_record(
        script_id="demo_script_01",
        historical_figure="Figura de prueba",
        script_text="Guion de prueba para validar la integración.",
        video_file_path="/path/final_video.mp4",
        voiceover_file_path="/path/voiceover_full.mp3",
        qa_status="aprobado",
        title="Título de prueba",
        description="Descripción de prueba.",
    )
    print(result)
