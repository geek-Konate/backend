import os
import uuid
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL ou SUPABASE_KEY manquant dans les variables d’environnement")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET = "portfolio-images"


def upload_image(file):
    # nom unique
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    # lire le contenu
    content = file.file.read()

    # upload dans Supabase
    result = supabase.storage.from_(BUCKET).upload(
        filename,
        content,
        {
            "content-type": file.content_type,
            "cache-control": "3600",
            "upsert": False
        }
    )

    # Supabase renvoie une erreur si ça échoue
    if hasattr(result, "error") and result.error:
        raise RuntimeError(result.error.message)

    # URL publique
    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{filename}"

    return public_url
