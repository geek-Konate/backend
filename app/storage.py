# app/storage.py
from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

# Crée le client Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
