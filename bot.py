import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import os
from datetime import datetime

# 1) İstersen yukarıda direkt token tanımla
TOKEN = "BURAYA_KENDİ_BOT_TOKENİNİ_YAZ"  # Kodu paylaşırken burada gerçek tokenını yazma!

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    if not hasattr(bot, "launch_time"):
        bot.launch_time = datetime.now()
    print(f"✅ {bot.user} ile giriş yapıldı ({len(bot.guilds)} sunucuda)")
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} slash komutu senkronize edildi!")
    except Exception as e:
        print(f"❌ Slash sync hatası: {e}")

# --- DUYURU KOMUTU ---
@bot.tree.command(name="duyuru", description="Ultra modern ve etkileşimli duyuru gönder")
@app_commands.describe(
    kanal="Duyuru gönderilecek kanal",
    mesaj="Duyuru içeriği",
    renk="Renk (örn: mavi, mor, altın, #hex)",
    banner="Banner veya gif url (opsiyonel)"
)
async def duyuru(
    interaction: discord.Interaction,
    kanal: discord.TextChannel,
    mesaj: str,
    renk: str = "mavi",
    banner: str = None
):
    renk_map = {
        "mavi": 0x1e90ff,
        "mor": 0x8e44ad,
        "altın": 0xf1c40f,
        "kırmızı": 0xe74c3c,
        "yeşil": 0x27ae60
    }
    if renk.startswith("#"):
        try:
            renk_deger = int(renk.replace("#", "0x"), 16)
        except:
            renk_deger = 0x1e90ff
    else:
        renk_deger = renk_map.get(renk.lower(), 0x1e90ff)

    embed = discord.Embed(
        title="📢 **YENİ DUYURU!**",
        description=f"> {mesaj}",
        color=renk_deger,
        timestamp=datetime.utcnow()
    )
    embed.set_author(
        name=f"{interaction.user.display_name}",
        icon_url=interaction.user.avatar.url if interaction.user.avatar else None
    )
    if banner:
        embed.set_image(url=banner)
    embed.set_footer(
        text=f"{interaction.user.display_name} • {datetime.utcnow().strftime('%d.%m.%Y %H:%M')}",
        icon_url=bot.user.avatar.url if bot.user.avatar else None
    )

    class OkudumView(View):
        def __init__(self):
            super().__init__(timeout=None)
            self.okuyanlar = set()
            self.msg_ref = None

        @discord.ui.button(label="Okudum!", style=discord.ButtonStyle.success, emoji="✅")
        async def okudum(self, interaction_buton: discord.Interaction, button: Button):
            user = interaction_buton.user
            if user.id in self.okuyanlar:
                await interaction_buton.response.send_message("Zaten okudun! 👍", ephemeral=True)
                return
            self.okuyanlar.add(user.id)
            await interaction_buton.response.send_message("Duyuru okundu olarak işaretlendi! 🙌", ephemeral=True)
            liste = ", ".join(f"<@{k}>" for k in self.okuyanlar)
            embed_new = self.msg_ref.embeds[0].copy()
            embed_new.clear_fields()
            if liste:
                embed_new.add_field(name="Okuyanlar", value=liste, inline=False)
            await self.msg_ref.edit(embed=embed_new, view=self)

    view = OkudumView()
    msg = await kanal.send(embed=embed, view=view)
    view.msg_ref = msg
    await interaction.response.send_message(f"✅ Duyuru {kanal.mention} kanalına gönderildi!", ephemeral=True)

# --- PING KOMUTU ---
@bot.tree.command(name="ping", description="Botun pingini gösterir")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot gecikmesi: **{latency}ms**",
        color=0x1e90ff,
        timestamp=datetime.utcnow()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

# --- SİSTEM BİLGİSİ KOMUTU ---
@bot.tree.command(name="sistem-bilgi", description="Botun çalıştığı ortamın sistem raporu")
async def sistem_bilgi(interaction: discord.Interaction):
    await interaction.response.send_message("🔄 Sistem bilgisi alınıyor...", ephemeral=True)
    try:
        import psutil
        import platform
        import sys
        uptime = datetime.now() - bot.launch_time if hasattr(bot, "launch_time") else None
        uptime_str = str(uptime).split('.')[0] if uptime else "?"
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        ping = round(bot.latency * 1000)
        users = sum(g.member_count for g in bot.guilds if g.member_count)
        embed = discord.Embed(
            title="🖥️ Sistem Bilgisi",
            description=f"**Platform:** `{platform.system()} {platform.release()}`\n"
                        f"**Mimari:** `{platform.machine()}`\n"
                        f"**Python:** `{platform.python_version()}`\n"
                        f"**discord.py:** `{discord.__version__}`",
            color=0x00ff41,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Bot Kullanıcı", value=f"`{bot.user}`", inline=True)
        embed.add_field(name="Çalışma Süresi", value=f"`{uptime_str}`", inline=True)
        embed.add_field(name="Sunucu", value=f"`{len(bot.guilds)}`", inline=True)
        embed.add_field(name="Kullanıcı", value=f"`{users}`", inline=True)
        embed.add_field(name="Ping", value=f"`{ping}ms`", inline=True)
        embed.add_field(
            name="CPU Kullanımı",
            value=f"`%{cpu_percent}`",
            inline=True
        )
        embed.add_field(
            name="RAM Kullanımı",
            value=f"`{memory.percent}%` ({memory.used//(1024**2)}MB / {memory.total//(1024**2)}MB)",
            inline=True
        )
        embed.add_field(
            name="Disk Kullanımı",
            value=f"`{disk.percent}%` ({disk.used//(1024**3)}GB / {disk.total//(1024**3)}GB)",
            inline=True
        )
        embed.set_footer(
            text=f"Komutu kullanan: {interaction.user.display_name}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )
        await interaction.edit_original_response(content=None, embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="❌ Sistem Bilgisi Hatası",
            description=f"```{str(e)}```",
            color=0xff0000
        )
        await interaction.edit_original_response(content=None, embed=embed)

# --- BOT BAŞLATMA ve TOKEN KONTROLÜ ---
if __name__ == "__main__":
    # Önce environment variable kontrolü
    token = os.getenv('BOT_TOKEN')
    # Eğer environment variable yoksa, yukarıdaki TOKEN değişkenini kullan
    if (token is None) or (len(token) < 10):  # 10’dan kısa ise yok say
        token = TOKEN
    # Son bir kez daha kontrol et
    if not token or len(token) < 50:
        print("❌ BOT_TOKEN eksik veya hatalı!")
        print("💡 Railway'de BOT_TOKEN variable'ını eklediğinizden emin olun")
        print("🔧 Token formatı: MTM5MzY1NzA1...")
        exit(1)
    try:
        print("🚀 Ultra Bot başlatılıyor...")
        print("🔥 Tüm sistemler hazır!")
        bot.run(token)
    except discord.LoginFailure:
        print("❌ Bot token'ı geçersiz!")
        print("💡 Discord Developer Portal'dan yeni token alın")
    except Exception as e:
        print(f"❌ Bot başlatılamadı: {e}")
