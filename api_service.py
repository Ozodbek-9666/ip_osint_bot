import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("BIGDATA_API_KEY")

async def get_ip_info(ip_address: str):
    # To'liq ma'lumot beruvchi endpoint
    url = "https://api.bigdatacloud.net/data/ip-geolocation-full"
    
    params = {
        "ip": ip_address,
        "key": API_KEY,
        "localityLanguage": "en",
        "localityInfo": "true"  # Bu tuman va ma'muriy hududlarni qo'shadi
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, timeout=15) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"DEBUG: Status {response.status}")
                    return None
        except Exception as e:
            print(f"DEBUG: Error: {e}")
            return None

def format_text_report(data):
    if not data:
        return "Ma'lumot topilmadi."

    # Ma'lumotlarni xavfsiz olish
    location = data.get('location', {})
    country = data.get('country', {})
    hazard = data.get('hazardReport', {})
    network = data.get('network', {})
    
    # Bayroq emoji va davlat nomi
    flag = country.get('countryFlagEmoji', '🌐')
    country_name = country.get('name', 'N/A')

    report = (
        f"🌐 **IP Details:** `{data.get('ip')}`\n\n"
        f"📍 **Location:**\n"
        f"├ City: {location.get('city', 'N/A')}\n"
        f"├ Locality: {location.get('localityName', 'N/A')}\n"
        f"├ Country: {flag} {country_name}\n"
        f"└ Coordinates: `{location.get('latitude', 0)}, {location.get('longitude', 0)}`\n\n"
        f"🛡 **Security Report:**\n"
        f"├ VPN: {'⚠️ Ha' if hazard.get('isKnownAsVpn') else '✅ Yo\'q'}\n"
        f"├ Proxy: {'⚠️ Ha' if hazard.get('isKnownAsProxy') else '✅ Yo\'q'}\n"
        f"├ Tor: {'⚠️ Ha' if hazard.get('isKnownAsTorServer') else '✅ Yo\'q'}\n"
        f"└ Hosting: {hazard.get('hostingLikelihood', 0)}%\n\n"
        f"📡 **Network:**\n"
        f"├ Org: {network.get('organisation', 'N/A')}\n"
        f"└ ASN: {network.get('carriers', [{}])[0].get('asn', 'N/A') if network.get('carriers') else 'N/A'}"
    )
    return report