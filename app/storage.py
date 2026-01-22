# app/storage.py
try:
    from supabase import create_client
    from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

    if SUPABASE_URL and SUPABASE_SERVICE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    else:
        print("⚠️ Variables Supabase non configurées")
        supabase = None
except ImportError:
    print("⚠️ Module supabase non installé")
    supabase = None
except Exception as e:
    print(f"⚠️ Erreur initialisation Supabase: {e}")
    supabase = None