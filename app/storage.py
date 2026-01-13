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
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    supabase.storage.from_("screenshots").upload(
        filename,
        file.file.read(),
        {"content-type": file.content_type}
    )

    return supabase.storage.from_("screenshots").get_public_url(filename).public_url

