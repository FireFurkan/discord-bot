diff --git a/bot.py b/bot.py
index 0f3a0c10d01a1ab63bd5418479f0c3a835252902..4916279cd29d928bba56b1f00bc1dbfbb9ed9e90 100644
--- a/bot.py
+++ b/bot.py
@@ -1,65 +1,90 @@
-import discord
-from discord.ext import commands
-from discord import app_commands
-from discord.ui import View, Button
-import os
-from datetime import datetime
+import logging
+import os
+from datetime import datetime
+
+import discord
+from discord import app_commands
+from discord.ext import commands
+from discord.ui import View, Button
+from dotenv import load_dotenv
 
-# 1) İstersen yukarıda direkt token tanımla
-TOKEN = "BURAYA_KENDİ_BOT_TOKENİNİ_YAZ"  # Kodu paylaşırken burada gerçek tokenını yazma!
+# .env dosyasından değişkenleri yükle
+load_dotenv()
+
+# Token ve prefix'i ortam değişkenlerinden al
+BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
+owner = os.getenv("BOT_OWNER_ID")
+BOT_OWNER_ID = int(owner) if owner and owner.isdigit() else None
 
-intents = discord.Intents.default()
-intents.message_content = True
-bot = commands.Bot(command_prefix="!", intents=intents)
+logging.basicConfig(level=logging.INFO)
+
+intents = discord.Intents.default()
+intents.message_content = True
+bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)
+bot.owner_id = BOT_OWNER_ID
 
 @bot.event
-async def on_ready():
+async def on_ready():
     if not hasattr(bot, "launch_time"):
         bot.launch_time = datetime.now()
     print(f"✅ {bot.user} ile giriş yapıldı ({len(bot.guilds)} sunucuda)")
     try:
         synced = await bot.tree.sync()
         print(f"✅ {len(synced)} slash komutu senkronize edildi!")
     except Exception as e:
-        print(f"❌ Slash sync hatası: {e}")
+        print(f"❌ Slash sync hatası: {e}")
+
+
+@bot.event
+async def on_command_error(ctx, error):
+    if isinstance(error, commands.CommandNotFound):
+        return
+    logging.error("Komut hatası: %s", error)
+    if isinstance(ctx, commands.Context):
+        await ctx.send(f"❌ Hata: {error}")
 
 # --- DUYURU KOMUTU ---
 @bot.tree.command(name="duyuru", description="Ultra modern ve etkileşimli duyuru gönder")
 @app_commands.describe(
     kanal="Duyuru gönderilecek kanal",
     mesaj="Duyuru içeriği",
     renk="Renk (örn: mavi, mor, altın, #hex)",
     banner="Banner veya gif url (opsiyonel)"
 )
-async def duyuru(
-    interaction: discord.Interaction,
-    kanal: discord.TextChannel,
-    mesaj: str,
-    renk: str = "mavi",
-    banner: str = None
-):
+async def duyuru(
+    interaction: discord.Interaction,
+    kanal: discord.TextChannel,
+    mesaj: str,
+    renk: str = "mavi",
+    banner: str = None
+):
+    if not interaction.user.guild_permissions.administrator:
+        await interaction.response.send_message(
+            "❌ Bu komutu kullanmak için yetkin yok.", ephemeral=True
+        )
+        return
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
diff --git a/bot.py b/bot.py
index 0f3a0c10d01a1ab63bd5418479f0c3a835252902..4916279cd29d928bba56b1f00bc1dbfbb9ed9e90 100644
--- a/bot.py
+++ b/bot.py
@@ -75,60 +100,87 @@ async def duyuru(
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
-@bot.tree.command(name="ping", description="Botun pingini gösterir")
-async def ping(interaction: discord.Interaction):
-    latency = round(bot.latency * 1000)
-    embed = discord.Embed(
-        title="🏓 Pong!",
-        description=f"Bot gecikmesi: **{latency}ms**",
-        color=0x1e90ff,
-        timestamp=datetime.utcnow()
-    )
-    await interaction.response.send_message(embed=embed, ephemeral=True)
+@bot.tree.command(name="ping", description="Botun pingini gösterir")
+@app_commands.describe(gizli="Cevap sadece sana görünsün")
+async def ping(interaction: discord.Interaction, gizli: bool = False):
+    latency = round(bot.latency * 1000)
+    embed = discord.Embed(
+        title="🏓 Pong!",
+        description=f"Bot gecikmesi: **{latency}ms**",
+        color=0x1e90ff,
+        timestamp=datetime.utcnow()
+    )
+    await interaction.response.send_message(embed=embed, ephemeral=gizli)
+
+
+# --- UPTIME KOMUTU ---
+@bot.tree.command(name="uptime", description="Botun çalışma süresini gösterir")
+async def uptime_cmd(interaction: discord.Interaction):
+    uptime = datetime.now() - bot.launch_time if hasattr(bot, "launch_time") else None
+    uptime_str = str(uptime).split(".")[0] if uptime else "?"
+    embed = discord.Embed(
+        title="⏱️ Uptime",
+        description=f"Bot {uptime_str} süredir aktif",
+        color=0x1e90ff,
+        timestamp=datetime.utcnow(),
+    )
+    await interaction.response.send_message(embed=embed, ephemeral=True)
+
+
+# --- SHUTDOWN KOMUTU ---
+@bot.tree.command(name="shutdown", description="Botu güvenli şekilde kapat")
+async def shutdown_cmd(interaction: discord.Interaction):
+    if interaction.user.id != bot.owner_id:
+        await interaction.response.send_message(
+            "❌ Bu komutu sadece bot sahibi kullanabilir.", ephemeral=True
+        )
+        return
+    await interaction.response.send_message("🛑 Bot kapatılıyor...", ephemeral=True)
+    await bot.close()
 
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
diff --git a/bot.py b/bot.py
index 0f3a0c10d01a1ab63bd5418479f0c3a835252902..4916279cd29d928bba56b1f00bc1dbfbb9ed9e90 100644
--- a/bot.py
+++ b/bot.py
@@ -144,46 +196,49 @@ async def sistem_bilgi(interaction: discord.Interaction):
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
-if __name__ == "__main__":
-    # Önce environment variable kontrolü
-    token = os.getenv('BOT_TOKEN')
-    # Eğer environment variable yoksa, yukarıdaki TOKEN değişkenini kullan
-    if (token is None) or (len(token) < 10):  # 10’dan kısa ise yok say
-        token = TOKEN
-    # Son bir kez daha kontrol et
-    if not token or len(token) < 50:
-        print("❌ BOT_TOKEN eksik veya hatalı!")
-        print("💡 Railway'de BOT_TOKEN variable'ını eklediğinizden emin olun")
-        print("🔧 Token formatı: MTM5MzY1NzA1...")
-        exit(1)
-    try:
-        print("🚀 Ultra Bot başlatılıyor...")
-        print("🔥 Tüm sistemler hazır!")
-        bot.run(token)
-    except discord.LoginFailure:
-        print("❌ Bot token'ı geçersiz!")
-        print("💡 Discord Developer Portal'dan yeni token alın")
-    except Exception as e:
-        print(f"❌ Bot başlatılamadı: {e}")
+if __name__ == "__main__":
+    # Token kontrolü
+    token = os.getenv('BOT_TOKEN')
+
+    if token is None:
+        print("❌ BOT_TOKEN environment variable bulunamadı!")
+        print("💡 Railway'de BOT_TOKEN variable'ını eklediğinizden emin olun")
+        print("🔧 Token formatı: MTM5MzY1NzA1...")
+        exit(1)
+
+    if len(token) < 50:
+        print("❌ BOT_TOKEN çok kısa görünüyor!")
+        print("💡 Doğru Discord bot token'ını kullandığınızdan emin olun")
+        exit(1)
+
+    try:
+        print("🚀 Ultra Bot başlatılıyor...")
+        print("🔥 Tüm sistemler hazır!")
+        bot.run(token)
+    except discord.LoginFailure:
+        print("❌ Bot token'ı geçersiz!")
+        print("💡 Discord Developer Portal'dan yeni token alın")
+    except Exception as e:
+        print(f"❌ Bot başlatılamadı: {e}")
