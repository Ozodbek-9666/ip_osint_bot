import json
import io
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile
from api_service import get_ip_info, format_text_report
import os
from database import add_user, get_stats
from dotenv import load_dotenv


load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID"))

router = Router()
user_data_storage = {}

def get_ip_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="📋 Ma'lumot", callback_data="view_text"),
        types.InlineKeyboardButton(text="🗺 Xarita", callback_data="view_map"),
        types.InlineKeyboardButton(text="📄 JSON", callback_data="view_json")
    )
    return builder.as_markup()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    # Foydalanuvchini bazaga qo'shish
    add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.answer("Salom! IP-manzil yuboring, men uni tahlil qilaman.")
    
@router.message(Command("stats"))
async def stats_handler(message: types.Message):
    # Faqat admin ko'ra oladi
    if message.from_user.id == ADMIN_ID:
        count, users = get_stats()
        user_list = "\n".join([f"👤 @{u[0]} ({u[1]})" for u in users if u[0]])
        await message.answer(f"📊 **Bot Statistikasi:**\n\n"
                             f"👥 Jami foydalanuvchilar: {count}\n\n"
                             f"📝 Oxirgi foydalanuvchilar:\n{user_list}")
    else:
        await message.answer("Siz admin emassiz!")
@router.message()
async def handle_ip(message: types.Message):
    ip = message.text.strip()
    # IP formatini tekshirish
    if not ip.replace('.', '').replace(':', '').isalnum():
        return
    if "." not in ip and ":" not in ip:
        await message.answer("⚠️ Iltimos, to'g'ri IP manzil yuboring (IPv4 yoki IPv6).")
        return
    data = await get_ip_info(ip)
    
    if data:
        user_data_storage[message.from_user.id] = data
        text = format_text_report(data)
        await message.answer(text, parse_mode="Markdown", reply_markup=get_ip_kb())
    else:
        await message.answer("❌ IP bo'yicha ma'lumot olishda xatolik yuz berdi.")

@router.callback_query(F.data == "view_json")
async def show_json(callback: types.CallbackQuery):
    data = user_data_storage.get(callback.from_user.id)
    
    if data:
        # 1. JSONni chiroyli (indent=4) matnga aylantiramiz
        json_text = json.dumps(data, indent=4, ensure_ascii=False)
        
        # 2. .txt fayl sifatida tayyorlash
        file_content = json_text.encode("utf-8")
        filename = f"osint_report_{data.get('ip')}.txt"
        text_file = BufferedInputFile(file_content, filename=filename)
        
        # 3. Faylni yuborish
        await callback.message.answer_document(
            document=text_file,
            caption=f"📄 {data.get('ip')} manzili bo'yicha JSON strukturadagi TXT hisoboti."
        )
        await callback.answer()
    else:
        await callback.answer("Ma'lumot topilmadi.", show_alert=True)

@router.callback_query(F.data == "view_text")
async def show_text(callback: types.CallbackQuery):
    data = user_data_storage.get(callback.from_user.id)
    if data:
        text = format_text_report(data)
        try:
            await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_ip_kb())
        except TelegramBadRequest:
            pass
    await callback.answer()

@router.callback_query(F.data == "view_map")
async def show_map(callback: types.CallbackQuery):
    data = user_data_storage.get(callback.from_user.id)
    if data:
        loc = data.get('location', {})
        lat, lon = loc.get('latitude'), loc.get('longitude')
        map_url = f"https://www.google.com/maps?q={lat},{lon}"
        
        text = (
            f"📍 **Koordinatalar:** `{lat}, {lon}`\n"
            f"🌍 **Hudud:** {loc.get('localityName', 'N/A')}\n\n"
            f"[Google Maps orqali ko'rish]({map_url})"
        )
        try:
            await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_ip_kb())
        except TelegramBadRequest:
            pass
    await callback.answer()