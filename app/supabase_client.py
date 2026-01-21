import os
from supabase import create_client , Client

from app.storage import SUPABASE_URL, supabase

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_API_KEY = os.getenv('SUPABASE_API_KEY')
supabase : client = create_client(SUPABASE_URL , SUPABASE_API_KEY)