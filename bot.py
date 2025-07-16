 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/bot.py b/bot.py
index 4916279cd29d928bba56b1f00bc1dbfbb9ed9e90..f7f6faebce07b68254ca9ea7b9c3d4e0c66ca789 100644
--- a/bot.py
+++ b/bot.py
@@ -1,69 +1,80 @@
 import logging
 import os
 from datetime import datetime
 
 import discord
 from discord import app_commands
 from discord.ext import commands
 from discord.ui import View, Button
 from dotenv import load_dotenv
 
 # .env dosyasından değişkenleri yükle
 load_dotenv()
 
 # Token ve prefix'i ortam değişkenlerinden al
 BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
 owner = os.getenv("BOT_OWNER_ID")
 BOT_OWNER_ID = int(owner) if owner and owner.isdigit() else None
 
-logging.basicConfig(level=logging.INFO)
+debug = os.getenv("DEBUG", "0").lower() in ("1", "true", "yes")
+logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
 
 intents = discord.Intents.default()
 intents.message_content = True
 bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)
 bot.owner_id = BOT_OWNER_ID
 
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
 
 
 @bot.event
 async def on_command_error(ctx, error):
     if isinstance(error, commands.CommandNotFound):
         return
     logging.error("Komut hatası: %s", error)
     if isinstance(ctx, commands.Context):
         await ctx.send(f"❌ Hata: {error}")
+
+
+@bot.event
+async def on_guild_join(guild: discord.Guild):
+    logging.info("Joined guild: %s (%s members)", guild.name, guild.member_count)
+
+
+@bot.event
+async def on_guild_remove(guild: discord.Guild):
+    logging.info("Removed from guild: %s", guild.name)
 
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
     if not interaction.user.guild_permissions.administrator:
         await interaction.response.send_message(
             "❌ Bu komutu kullanmak için yetkin yok.", ephemeral=True
         )
         return
     renk_map = {
         "mavi": 0x1e90ff,
         "mor": 0x8e44ad,
         "altın": 0xf1c40f,
diff --git a/bot.py b/bot.py
index 4916279cd29d928bba56b1f00bc1dbfbb9ed9e90..f7f6faebce07b68254ca9ea7b9c3d4e0c66ca789 100644
--- a/bot.py
+++ b/bot.py
@@ -127,50 +138,85 @@ async def duyuru(
 async def ping(interaction: discord.Interaction, gizli: bool = False):
     latency = round(bot.latency * 1000)
     embed = discord.Embed(
         title="🏓 Pong!",
         description=f"Bot gecikmesi: **{latency}ms**",
         color=0x1e90ff,
         timestamp=datetime.utcnow()
     )
     await interaction.response.send_message(embed=embed, ephemeral=gizli)
 
 
 # --- UPTIME KOMUTU ---
 @bot.tree.command(name="uptime", description="Botun çalışma süresini gösterir")
 async def uptime_cmd(interaction: discord.Interaction):
     uptime = datetime.now() - bot.launch_time if hasattr(bot, "launch_time") else None
     uptime_str = str(uptime).split(".")[0] if uptime else "?"
     embed = discord.Embed(
         title="⏱️ Uptime",
         description=f"Bot {uptime_str} süredir aktif",
         color=0x1e90ff,
         timestamp=datetime.utcnow(),
     )
     await interaction.response.send_message(embed=embed, ephemeral=True)
 
 
+# --- AVATAR KOMUTU ---
+@bot.tree.command(name="avatar", description="Kullanıcının avatarını gösterir")
+@app_commands.describe(kullanici="Hedef kullanıcı")
+async def avatar_cmd(interaction: discord.Interaction, kullanici: discord.User = None):
+    user = kullanici or interaction.user
+    embed = discord.Embed(
+        title=f"{user.display_name} Avatarı",
+        color=0x1e90ff,
+        timestamp=datetime.utcnow(),
+    )
+    if user.avatar:
+        embed.set_image(url=user.avatar.url)
+    else:
+        embed.description = "Kullanıcının avatarı bulunamadı."
+    await interaction.response.send_message(embed=embed, ephemeral=True)
+
+
+# --- SERVER INFO KOMUTU ---
+@bot.tree.command(name="server-info", description="Bulunduğun sunucu bilgilerini gösterir")
+async def server_info(interaction: discord.Interaction):
+    guild = interaction.guild
+    if guild is None:
+        await interaction.response.send_message("❌ Bu komut DM'de kullanılamaz.", ephemeral=True)
+        return
+    embed = discord.Embed(
+        title=guild.name,
+        color=0x1e90ff,
+        timestamp=datetime.utcnow(),
+    )
+    embed.add_field(name="Üye Sayısı", value=guild.member_count, inline=True)
+    embed.add_field(name="Oluşturulma", value=guild.created_at.strftime('%d.%m.%Y %H:%M'), inline=True)
+    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
+    await interaction.response.send_message(embed=embed, ephemeral=True)
+
+
 # --- SHUTDOWN KOMUTU ---
 @bot.tree.command(name="shutdown", description="Botu güvenli şekilde kapat")
 async def shutdown_cmd(interaction: discord.Interaction):
     if interaction.user.id != bot.owner_id:
         await interaction.response.send_message(
             "❌ Bu komutu sadece bot sahibi kullanabilir.", ephemeral=True
         )
         return
     await interaction.response.send_message("🛑 Bot kapatılıyor...", ephemeral=True)
     await bot.close()
 
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
 
EOF
)
