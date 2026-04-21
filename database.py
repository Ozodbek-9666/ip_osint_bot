import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Supabase ulanish ma'lumotlari
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_user(user_id, username, full_name, phone_number=None):
    """
    Foydalanuvchini bazaga qo'shish yoki yangilash.
    Telefon raqami ixtiyoriy (agar startda so'ralsa).
    """
    data = {
        "user_id": user_id,
        "username": username,
        "full_name": full_name,
        "phone_number": phone_number
    }
    # upsert - foydalanuvchi bo'lsa yangilaydi, bo'lmasa qo'shadi
    try:
        supabase.table("users").upsert(data).execute()
    except Exception as e:
        print(f"Baza bilan ishlashda xatolik: {e}")

def get_stats():
    """
    Umumiy foydalanuvchilar soni va ro'yxatini olish.
    """
    try:
        # Hamma ma'lumotlarni va aniq sonini olamiz
        response = supabase.table("users").select("*", count="exact").execute()
        count = response.count
        users_list = response.data
        return count, users_list
    except Exception as e:
        print(f"Statistika olishda xatolik: {e}")
        return 0, []