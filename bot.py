import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot başlangıç zamanını kaydet
bot.start_time = datetime.now()

# Basit Grow A Tycoon durumu (Rate Limit Yok)
async def typing_effect_grow_tycoon():
    try:
        print('🎮 Basit durum sistemi başlatıldı')
        
        while True:  # SONSUZ DÖNGÜ
            # Sadece 3 durum arasında geçiş (rate limit önleme)
            statuses = [
                "Grow A Tycoon oynuyor ✨",
                "🎮 Grow A Tycoon",
                "Grow A Tycoon 🎯"
            ]
            
            for status in statuses:
                await bot.change_presence(
                    activity=discord.Game(name=status),
                    status=discord.Status.online
                )
                # Her durum değişimi arasında 2 dakika bekle (Discord API güvenli)
                await asyncio.sleep(120)  # 2 dakika = 120 saniye
            
    except Exception as e:
        print(f'❌ Durum sistemi durdu: {e}')
        # Hata durumunda 5 dakika bekle
        await asyncio.sleep(300)
        await typing_effect_grow_tycoon()

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')
    print(f'Bot {len(bot.guilds)} sunucuda aktif')
    
    # Typing efektini arka planda başlat (bloke etmesin)
    asyncio.create_task(typing_effect_grow_tycoon())
    
    # GLOBAL slash komut senkronizasyonu (daha güvenilir)
    try:
        synced = await bot.tree.sync()
        print(f'✅ {len(synced)} slash komutu GLOBAL olarak senkronize edildi')
        
        # Ayrıca guild-specific de dene
        if bot.guilds:
            guild = bot.guilds[0]
            guild_synced = await bot.tree.sync(guild=guild)
            print(f'✅ {len(guild_synced)} slash komutu {guild.name} sunucusuna senkronize edildi')
            
    except Exception as e:
        print(f'❌ Slash komut senkronizasyon hatası: {e}')
        
        # Hata durumunda tekrar dene
        try:
            await asyncio.sleep(5)
            synced = await bot.tree.sync()
            print(f'✅ İkinci deneme: {len(synced)} slash komutu senkronize edildi')
        except Exception as e2:
            print(f'❌ İkinci deneme de başarısız: {e2}')

# Slash Command: /mesaj (GÜZELLEŞTİRİLMİŞ EFEKTLİ)
@bot.tree.command(name="mesaj", description="Gelişmiş embed mesaj gönder")
@app_commands.describe(
    kanal="Mesajın gönderileceği kanal",
    mesaj="Gönderilecek mesaj içeriği", 
    gonderen="Mesajı gönderen kişi",
    baslik="Mesaj başlığı (opsiyonel)",
    renk="Embed rengi (mavi/kırmızı/yeşil/altın/mor)",
    unvan="Gönderenin unvanı (varsayılan: Baş Bot Geliştirici)"
)
@app_commands.default_permissions(administrator=True)
@app_commands.choices(renk=[
    app_commands.Choice(name="Mavi", value="mavi"),
    app_commands.Choice(name="Kırmızı", value="kırmızı"),
    app_commands.Choice(name="Yeşil", value="yeşil"),
    app_commands.Choice(name="Altın", value="altın"),
    app_commands.Choice(name="Mor", value="mor"),
])
async def mesaj_komutu(
    interaction: discord.Interaction, 
    kanal: discord.TextChannel, 
    mesaj: str, 
    gonderen: discord.Member,
    baslik: str = None,
    renk: str = "mavi",
    unvan: str = "Baş Bot Geliştirici"
):
    # Renk seçimi
    renk_map = {
        "mavi": 0x1e90ff,
        "kırmızı": 0xff0000,
        "yeşil": 0x00ff00,
        "altın": 0xffd700,
        "mor": 0x8a2be2
    }
    
    # Embed oluştur
    embed = discord.Embed(
        title=baslik if baslik else None,
        description=mesaj,
        color=renk_map.get(renk, 0x1e90ff),
        timestamp=discord.utils.utcnow()
    )
    
    # Üst kısım - Bot bilgisi
    embed.set_author(
        name="İTF | Bot 🔧 UYG",
        icon_url=bot.user.avatar.url if bot.user.avatar else None
    )
    
    try:
        # İlk mesajı gönder (footer olmadan)
        sent_message = await kanal.send(
            embed=embed,
            allowed_mentions=discord.AllowedMentions(everyone=True, users=True, roles=True)
        )
        
        # Onay mesajı
        await interaction.response.send_message(
            f"✅ Mesaj gönderildi! Güzel efekt başlıyor...", 
            ephemeral=True
        )
        
        # GÜZEL UNVAN EFEKTİ BAŞLA!
        await beautiful_title_effect(sent_message, embed, gonderen, unvan)
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ Bu kanala mesaj göndermek için iznim yok!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Hata: {e}", ephemeral=True)

# GÜZEL UNVAN EFEKTİ FONKSİYONU
async def beautiful_title_effect(message, embed, gonderen, unvan):
    try:
        # 1. DOTS EFEKTİ
        dots_effects = [
            f"🔹 {gonderen.display_name}.",
            f"🔹 {gonderen.display_name}..",
            f"🔹 {gonderen.display_name}...",
            f"🔹 {gonderen.display_name}, yazıyor..."
        ]
        
        for dots in dots_effects:
            embed.set_footer(
                text=dots,
                icon_url=gonderen.avatar.url if gonderen.avatar else None
            )
            await message.edit(embed=embed)
            await asyncio.sleep(0.8)
        
        # 2. EMOJI ANİMASYON
        emoji_effects = [
            f"🔹 {gonderen.display_name}, 🎯 {unvan}",
            f"🔹 {gonderen.display_name}, ⚡ {unvan}",
            f"🔹 {gonderen.display_name}, 🔥 {unvan}",
            f"🔹 {gonderen.display_name}, ✨ {unvan}",
        ]
        
        for emoji_text in emoji_effects:
            embed.set_footer(
                text=emoji_text,
                icon_url=gonderen.avatar.url if gonderen.avatar else None
            )
            await message.edit(embed=embed)
            await asyncio.sleep(0.6)
        
        # 3. PROGRESS BAR EFEKTİ
        progress_effects = [
            f"🔹 {gonderen.display_name}, [■□□□□] {unvan}",
            f"🔹 {gonderen.display_name}, [■■□□□] {unvan}",
            f"🔹 {gonderen.display_name}, [■■■□□] {unvan}",
            f"🔹 {gonderen.display_name}, [■■■■□] {unvan}",
            f"🔹 {gonderen.display_name}, [■■■■■] {unvan}!",
        ]
        
        for progress in progress_effects:
            embed.set_footer(
                text=progress,
                icon_url=gonderen.avatar.url if gonderen.avatar else None
            )
            await message.edit(embed=embed)
            await asyncio.sleep(0.5)
        
        # 4. FINAL SPARKLE EFEKTİ
        sparkle_effects = [
            f"🔹 {gonderen.display_name}, ✨ {unvan} ✨",
            f"🔹 {gonderen.display_name}, 🌟 {unvan} 🌟",
            f"🔹 {gonderen.display_name}, 💫 {unvan} 💫",
            f"🔹 {gonderen.display_name}, ⭐ {unvan} ⭐",
        ]
        
        for sparkle in sparkle_effects:
            embed.set_footer(
                text=sparkle,
                icon_url=gonderen.avatar.url if gonderen.avatar else None
            )
            await message.edit(embed=embed)
            await asyncio.sleep(0.4)
        
        # 5. FINAL DURUM
        embed.set_footer(
            text=f"🔹 {gonderen.display_name}, {unvan} 👑",
            icon_url=gonderen.avatar.url if gonderen.avatar else None
        )
        await message.edit(embed=embed)
        
    except Exception as e:
        print(f"Unvan efekti hatası: {e}")

# Slash Command: /duyuru
@bot.tree.command(name="duyuru", description="Hızlı duyuru mesajı gönder")
@app_commands.describe(
    kanal="Duyuru kanalı",
    mesaj="Duyuru mesajı",
    gonderen="Duyuruyu yapan kişi"
)
@app_commands.default_permissions(administrator=True)
async def duyuru_komutu(interaction: discord.Interaction, kanal: discord.TextChannel, mesaj: str, gonderen: discord.Member):
    try:
        # Basit embed oluştur
        embed = discord.Embed(
            description=mesaj,
            color=0x1e90ff,
            timestamp=discord.utils.utcnow()
        )
        
        # Üst kısım
        embed.set_author(
            name="İTF | Bot 🔧 UYG",
            icon_url=bot.user.avatar.url if bot.user.avatar else None
        )
        
        # Alt kısım
        embed.set_footer(
            text=f"🔹 {gonderen.display_name}, Baş Bot Geliştirici ✨",
            icon_url=gonderen.avatar.url if gonderen.avatar else None
        )
        
        # Mesaj gönder
        await kanal.send(
            embed=embed,
            allowed_mentions=discord.AllowedMentions(everyone=True, users=True, roles=True)
        )
        
        # Onay mesajı
        await interaction.response.send_message(
            f"✅ Duyuru başarıyla {kanal.mention} kanalına gönderildi!", 
            ephemeral=True
        )
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ Kanala mesaj göndermek için iznim yok!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Hata: {e}", ephemeral=True)

# Slash Command: /sistem-bilgi (HIZLI VE STABIL)
@bot.tree.command(name="sistem-bilgi", description="Bot ve sistem detaylarını gösterir")
async def sistem_bilgi_komutu(interaction: discord.Interaction):
    import psutil
    import platform
    import sys
    from datetime import datetime, timedelta
    
    try:
        # ÖNCE HIZLI YANIT VER (Discord timeout önleme)
        await interaction.response.send_message("🔄 **Sistem bilgileri toplanıyor...**")
        
        # Başlangıç zamanını hesapla
        uptime = datetime.now() - bot.start_time
        uptime_str = str(uptime).split('.')[0]
        
        # Hızlı sistem bilgileri (timeout yok)
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        ping = round(bot.latency * 1000)
        total_users = sum(guild.member_count for guild in bot.guilds)
        total_commands = len([cmd for cmd in bot.tree.get_commands()])
        
        # GERÇEK AKTİF UYGULAMA TARAMA
        def get_real_active_apps():
            try:
                real_apps = []
                app_mapping = {
                    'robloxplayerbeta.exe': '🎮 Roblox Player',
                    'robloxstudio.exe': '🎮 Roblox Studio', 
                    'discord.exe': '💬 Discord',
                    'chrome.exe': '🌐 Google Chrome',
                    'firefox.exe': '🦊 Firefox',
                    'spotify.exe': '🎵 Spotify',
                    'steam.exe': '🎮 Steam',
                    'steamwebhelper.exe': '🎮 Steam Helper',
                    'minecraft.exe': '⛏️ Minecraft',
                    'javaw.exe': '☕ Java App',
                    'code.exe': '💻 VS Code',
                    'notepad.exe': '📝 Notepad',
                    'obs64.exe': '📹 OBS Studio',
                    'valorant.exe': '🔫 Valorant',
                    'valorant-win64-shipping.exe': '🔫 Valorant Game',
                    'leagueoflegends.exe': '⚔️ League of Legends',
                    'lol.exe': '⚔️ LoL Client',
                    'fortnitelient-win64-shipping.exe': '🏗️ Fortnite',
                    'epicgameslauncher.exe': '🎮 Epic Games',
                    'telegram.exe': '📱 Telegram',
                    'whatsapp.exe': '📱 WhatsApp',
                    'excel.exe': '📊 Excel',
                    'winword.exe': '📄 Word',
                    'powerpnt.exe': '📈 PowerPoint',
                    'csgo.exe': '🎯 CS:GO',
                    'gta5.exe': '🚗 GTA V',
                    'apex.exe': '🎯 Apex Legends',
                    'destiny2.exe': '🚀 Destiny 2',
                    'among us.exe': '🔍 Among Us',
                    'fallguys_client.exe': '🎪 Fall Guys'
                }
                
                # Gerçek process'leri tara
                for process in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                    try:
                        process_name = process.info['name'].lower()
                        cpu_usage = process.info['cpu_percent'] or 0
                        
                        # Eşleşen uygulamayı bul
                        for exe_name, display_name in app_mapping.items():
                            if process_name == exe_name.lower():
                                # Aynı uygulamadan birden fazla process varsa en yüksek CPU'lu olanı al
                                existing = next((app for app in real_apps if app[0] == display_name), None)
                                if not existing:
                                    real_apps.append((display_name, cpu_usage))
                                elif cpu_usage > existing[1]:
                                    real_apps.remove(existing)
                                    real_apps.append((display_name, cpu_usage))
                                break
                                
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
                
                # CPU kullanımına göre sırala ve en fazla 6 tane al
                real_apps.sort(key=lambda x: x[1], reverse=True)
                return real_apps[:6]
                
            except Exception as e:
                return [("❌ Tarama hatası", 0)]
        
        active_apps = get_real_active_apps()
        
        # Ana embed
        embed = discord.Embed(
            title="🖥️ **SİSTEM BİLGİLERİ**",
            description="```ansi\n\u001b[1;36m▬▬▬▬▬▬▬▬ İTTİFAK ORDUSU BOT ▬▬▬▬▬▬▬▬\u001b[0m```",
            color=0x00ff41,
            timestamp=discord.utils.utcnow()
        )
        
        # Bot Bilgileri
        embed.add_field(
            name="🤖 **BOT BİLGİLERİ**",
            value=f"""
```yaml
Uptime: {uptime_str}
Ping: {ping}ms
Sunucular: {len(bot.guilds)}
Kullanıcılar: {total_users:,}
Komutlar: {total_commands}
```""",
            inline=True
        )
        
        # Sistem Bilgileri
        embed.add_field(
            name="💻 **SİSTEM BİLGİLERİ**",
            value=f"""
```yaml
OS: {platform.system()} {platform.release()}
CPU: {cpu_percent}%
RAM: {memory.percent}% ({memory.used // (1024**3)}GB/{memory.total // (1024**3)}GB)
Disk: {disk.percent}%
```""",
            inline=True
        )
        
        # AKTİF UYGULAMALAR (GERÇEK TARAMA)
        if active_apps and active_apps[0][0] != "❌ Tarama hatası":
            app_text = ""
            for app_name, cpu_usage in active_apps:
                if cpu_usage > 0:
                    # CPU çubuğu (10 karakter)
                    cpu_bar_length = min(10, max(1, int(cpu_usage / 5)))  # Her 5% = 1 karakter
                    cpu_bar = "█" * cpu_bar_length + "░" * (10 - cpu_bar_length)
                    app_text += f"{app_name}\n`{cpu_bar}` **{cpu_usage:.1f}%** CPU\n"
                else:
                    app_text += f"{app_name}\n`░░░░░░░░░░` **0.0%** CPU\n"
            
            embed.add_field(
                name="🔥 **GERÇEK AKTİF UYGULAMALAR**",
                value=app_text[:1024] if app_text else "```Hiçbir uygulama aktif değil```",
                inline=True
            )
        else:
            embed.add_field(
                name="🔥 **AKTİF UYGULAMALAR**",
                value="```Hiçbir bilinen uygulama çalışmıyor```",
                inline=True
            )
        
        # Teknoloji Stack
        embed.add_field(
            name="⚡ **TEKNOLOJİ STACK**",
            value=f"""
```yaml
Python: {sys.version.split()[0]}
Discord.py: {discord.__version__}
Asyncio: ✅ Aktif
WebSocket: ✅ Bağlı
```""",
            inline=True
        )
        
        # Performans çubukları
        def create_bar(percentage, length=10):
            filled = int(length * percentage / 100)
            bar = "█" * filled + "░" * (length - filled)
            return f"`{bar}` {percentage}%"
        
        embed.add_field(
            name="📊 **SISTEM PERFORMANSI**",
            value=f"""
**CPU:** {create_bar(cpu_percent)}
**RAM:** {create_bar(memory.percent)}
**Disk:** {create_bar(disk.percent)}
""",
            inline=False
        )
        
        # Sistem durumu
        if cpu_percent < 50 and memory.percent < 70:
            system_status = "🟢 **EXCELLENT** - Sistem optimal çalışıyor"
        elif cpu_percent < 80 and memory.percent < 85:
            system_status = "🟡 **GOOD** - Sistem normal çalışıyor"
        else:
            system_status = "🔴 **WARNING** - Sistem yüksek yük altında"
            
        embed.add_field(
            name="🎯 **SİSTEM DURUMU**",
            value=system_status,
            inline=False
        )
        
        # En aktif uygulama (Eğer varsa)
        if active_apps and active_apps[0][0] != "❌ Tarama hatası" and active_apps[0][1] > 0:
            top_app = active_apps[0]
            if top_app[1] > 5:  # CPU > 5% ise göster
                embed.add_field(
                    name="🏆 **EN AKTİF UYGULAMA**",
                    value=f"""
**{top_app[0]}**
```yaml
CPU Kullanımı: {top_app[1]:.1f}%
Durum: {"Yoğun Çalışıyor" if top_app[1] > 20 else "Normal Çalışıyor"}
Process: Gerçek Zamanlı
```""",
                    inline=False
                )
        
        embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
        embed.set_footer(
            text=f"🔹 İsteyen: {interaction.user.display_name} • Gerçek Process Tarama",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )
        
        # Mesajı güncelle (timeout yok)
        await interaction.edit_original_response(content=None, embed=embed)
        
    except Exception as e:
        try:
            # Hata durumunda basit mesaj
            error_embed = discord.Embed(
                title="❌ Sistem Bilgisi Hatası",
                description=f"Detaylar alınamadı: `{str(e)[:100]}...`",
                color=0xff0000
            )
            await interaction.edit_original_response(content=None, embed=error_embed)
        except:
            pass

# Slash Command: /ping (PROFESYONEL)
@bot.tree.command(name="ping", description="Bot gecikme ve bağlantı kalitesini test eder")
async def ping_komutu(interaction: discord.Interaction):
    import time
    
    try:
        start_time = time.time()
        
        # İlk yanıt
        await interaction.response.send_message("🏓 **Ping ölçülüyor...**")
        
        # Response time hesapla
        response_time = (time.time() - start_time) * 1000
        
        # WebSocket gecikme
        ws_ping = round(bot.latency * 1000)
        
        # Ping kalitesi
        if ws_ping < 50:
            quality = "🟢 **Mükemmel**"
        elif ws_ping < 100:
            quality = "🟡 **İyi**"
        elif ws_ping < 200:
            quality = "🟠 **Orta**"
        else:
            quality = "🔴 **Yavaş**"
        
        embed = discord.Embed(
            title="🏓 **PING SONUÇLARI**",
            color=0x00ff00 if ws_ping < 100 else 0xffff00 if ws_ping < 200 else 0xff0000,
            timestamp=discord.utils.utcnow()
        )
        
        embed.add_field(name="⚡ WebSocket", value=f"```{ws_ping}ms```", inline=True)
        embed.add_field(name="🔄 Response", value=f"```{response_time:.0f}ms```", inline=True)
        embed.add_field(name="📊 Kalite", value=quality, inline=True)
        
        embed.set_footer(text=f"🔹 Test eden: {interaction.user.display_name}")
        
        await interaction.edit_original_response(content=None, embed=embed)
        
    except Exception as e:
        await interaction.edit_original_response(content=f"❌ Ping testi başarısız: `{e}`")

# Slash Command: /qr-kod
@bot.tree.command(name="qr-kod", description="Metni QR koda dönüştürür")
@app_commands.describe(metin="QR koda dönüştürülecek metin")
async def qr_kod_komutu(interaction: discord.Interaction, metin: str):
    import urllib.parse
    
    try:
        if len(metin) > 500:
            await interaction.response.send_message("❌ Metin çok uzun! Maksimum 500 karakter.", ephemeral=True)
            return
        
        await interaction.response.send_message("🔲 **QR kod oluşturuluyor...**")
        
        # QR kod URL'si
        encoded_text = urllib.parse.quote(metin)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_text}"
        
        embed = discord.Embed(
            title="🔲 **QR KOD OLUŞTURULDU**",
            description=f"```{metin[:100]}{'...' if len(metin) > 100 else ''}```",
            color=0x9932cc,
            timestamp=discord.utils.utcnow()
        )
        
        embed.set_image(url=qr_url)
        embed.set_footer(text=f"🔹 Oluşturan: {interaction.user.display_name}")
        
        await interaction.edit_original_response(content=None, embed=embed)
        
    except Exception as e:
        await interaction.edit_original_response(content=f"❌ QR kod hatası: `{e}`")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if 'merhaba' in message.content.lower():
        await message.channel.send(f'Merhaba {message.author.mention}! 👋')
    
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(name='bilgi')
async def bilgi(ctx):
    embed = discord.Embed(
        title="Bot Bilgileri",
        description="Bu bot Python ile yazılmıştır!",
        color=0x00ff00
    )
    embed.add_field(name="Sunucu Sayısı", value=len(bot.guilds), inline=True)
    embed.add_field(name="Kullanıcı Sayısı", value=len(bot.users), inline=True)
    await ctx.send(embed=embed)

# Token'ınızı buraya yazın
# ÖNEMLI: Gerekli kütüphaneler!
# Terminal'de şu komutları çalıştırın:
# pip install psutil
# pip install aiohttp
import os
bot.run(os.getenv('MTM5MzY1NzA1MDc4OTE4Nzc3NA.GM6QnF.y8oj-cTukZbDbV395lZbBqMXjqASqXth-1C30E'))