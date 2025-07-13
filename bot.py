import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
import time
import urllib.parse
from datetime import datetime

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot başlangıç zamanını kaydet
bot.start_time = datetime.now()

# GELIŞMIŞ GROW A TYCOON DURUM SİSTEMİ
async def advanced_status_system():
    """Gelişmiş durum sistemi - Grow A Tycoon temalı"""
    try:
        print('🎮 Gelişmiş durum sistemi başlatıldı')
        
        status_categories = {
            'gaming': [
                "🎮 Grow A Tycoon oynuyor",
                "💰 Para kazanıyor - Grow A Tycoon",
                "🏭 Fabrika kuruyor - Grow A Tycoon",
                "📈 İş imparatorluğu büyütüyor",
                "🎯 Grow A Tycoon - Seviye atlıyor"
            ],
            'work': [
                "⚡ Discord'u güçlendiriyor",
                "🔧 Sunucu yönetiyor",
                "📊 Verileri analiz ediyor",
                "🛡️ Güvenlik sağlıyor",
                "🚀 Performansı optimize ediyor"
            ],
            'fun': [
                "🎪 Kullanıcılarla eğleniyor",
                "🎭 Komutları sergiliyor",
                "🎨 Embed'ler tasarlıyor",
                "🎯 Hedefleri vuruyor",
                "✨ Sihir yapıyor"
            ]
        }
        
        while True:
            # Kategorileri döngüsel olarak değiştir
            for category, statuses in status_categories.items():
                for status in statuses:
                    await bot.change_presence(
                        activity=discord.Game(name=status),
                        status=discord.Status.online
                    )
                    await asyncio.sleep(180)  # 3 dakika bekle
                    
    except Exception as e:
        print(f'❌ Durum sistemi hatası: {e}')
        await asyncio.sleep(300)  # 5 dakika bekle ve tekrar başlat
        await advanced_status_system()

@bot.event
async def on_ready():
    print(f'🚀 {bot.user} olarak giriş yapıldı!')
    print(f'📊 {len(bot.guilds)} sunucuda aktif')
    print(f'👥 {len(bot.users)} kullanıcıya hizmet veriyor')
    
    # Gelişmiş durum sistemini başlat
    asyncio.create_task(advanced_status_system())
    
    # Slash komutları senkronize et
    try:
        synced = await bot.tree.sync()
        print(f'✅ {len(synced)} slash komutu GLOBAL olarak senkronize edildi')
        
        # Guild-specific senkronizasyon
        if bot.guilds:
            for guild in bot.guilds:
                try:
                    guild_synced = await bot.tree.sync(guild=guild)
                    print(f'✅ {len(guild_synced)} slash komutu {guild.name} sunucusuna senkronize edildi')
                except Exception as e:
                    print(f'⚠️ {guild.name} sunucusunda senkronizasyon hatası: {e}')
                    
    except Exception as e:
        print(f'❌ Slash komut senkronizasyon hatası: {e}')

# ULTRA GELİŞMİŞ MESAJ KOMUTU
@bot.tree.command(name="mesaj", description="🎨 Süper animasyonlu embed mesaj gönder")
@app_commands.describe(
    kanal="Mesajın gönderileceği kanal",
    mesaj="Gönderilecek mesaj içeriği", 
    gonderen="Mesajı gönderen kişi",
    baslik="Mesaj başlığı (opsiyonel)",
    renk="Embed rengi",
    unvan="Gönderenin unvanı",
    animasyon="Footer animasyon türü"
)
@app_commands.default_permissions(administrator=True)
@app_commands.choices(renk=[
    app_commands.Choice(name="💙 Mavi", value="mavi"),
    app_commands.Choice(name="❤️ Kırmızı", value="kirmizi"),
    app_commands.Choice(name="💚 Yeşil", value="yesil"),
    app_commands.Choice(name="💛 Altın", value="altin"),
    app_commands.Choice(name="💜 Mor", value="mor"),
    app_commands.Choice(name="🖤 Siyah", value="siyah")
])
@app_commands.choices(animasyon=[
    app_commands.Choice(name="✨ Klasik Efekt", value="klasik"),
    app_commands.Choice(name="🔥 Ateş Efekti", value="ates"),
    app_commands.Choice(name="⚡ Şimşek Efekti", value="simsek"),
    app_commands.Choice(name="🌟 Yıldız Efekti", value="yildiz")
])
async def ultra_mesaj_komutu(
    interaction: discord.Interaction, 
    kanal: discord.TextChannel, 
    mesaj: str, 
    gonderen: discord.Member,
    baslik: str = None,
    renk: str = "mavi",
    unvan: str = "🏆 Süper Yönetici",
    animasyon: str = "klasik"
):
    # Gelişmiş renk paleti
    renk_map = {
        "mavi": 0x1e90ff,
        "kirmizi": 0xff0000,
        "yesil": 0x00ff00,
        "altin": 0xffd700,
        "mor": 0x8a2be2,
        "siyah": 0x2c2c2c
    }
    
    # Embed oluştur
    embed = discord.Embed(
        title=f"📢 {baslik}" if baslik else "📢 Önemli Mesaj",
        description=mesaj,
        color=renk_map.get(renk, 0x1e90ff),
        timestamp=datetime.utcnow()
    )
    
    # Süper author tasarımı
    embed.set_author(
        name="🎭 İTTİFAK ORDUSU | BOT SİSTEMİ",
        icon_url=bot.user.avatar.url if bot.user.avatar else None
    )
    
    try:
        # İlk mesajı gönder
        sent_message = await kanal.send(embed=embed)
        
        # Onay mesajı
        await interaction.response.send_message(
            f"✅ Mesaj gönderildi! 🎬 {animasyon.title()} animasyonu başlıyor...", 
            ephemeral=True
        )
        
        # SÜper animasyon efektini başlat
        await ultra_animation_effect(sent_message, embed, gonderen, unvan, animasyon)
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ Bu kanala mesaj göndermek için iznim yok!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Hata: {e}", ephemeral=True)

# ULTRA ANİMASYON EFEKTLERİ
async def ultra_animation_effect(message, embed, gonderen, unvan, animasyon_turu):
    """Süper gelişmiş animasyon efektleri"""
    try:
        if animasyon_turu == "klasik":
            await klasik_animasyon(message, embed, gonderen, unvan)
        elif animasyon_turu == "ates":
            await ates_animasyonu(message, embed, gonderen, unvan)
        elif animasyon_turu == "simsek":
            await simsek_animasyonu(message, embed, gonderen, unvan)
        elif animasyon_turu == "yildiz":
            await yildiz_animasyonu(message, embed, gonderen, unvan)
    except Exception as e:
        print(f"Animasyon hatası: {e}")

async def klasik_animasyon(message, embed, gonderen, unvan):
    """Klasik typing efekti"""
    effects = [
        f"🔹 {gonderen.display_name}",
        f"🔹 {gonderen.display_name}.",
        f"🔹 {gonderen.display_name}..",
        f"🔹 {gonderen.display_name}...",
        f"🔸 {gonderen.display_name}, yazıyor...",
        f"🔶 {gonderen.display_name}, {unvan}",
        f"🔷 {gonderen.display_name}, ⚡ {unvan}",
        f"💎 {gonderen.display_name}, ✨ {unvan} ✨",
        f"👑 {gonderen.display_name}, 🏆 {unvan} 🏆"
    ]
    
    for effect in effects:
        embed.set_footer(text=effect, icon_url=gonderen.avatar.url if gonderen.avatar else None)
        await message.edit(embed=embed)
        await asyncio.sleep(0.7)

async def ates_animasyonu(message, embed, gonderen, unvan):
    """Ateş efekti"""
    fire_effects = [
        f"🔥 {gonderen.display_name}",
        f"🔥🔥 {gonderen.display_name}",
        f"🔥🔥🔥 {gonderen.display_name}, yanıyor...",
        f"🌋 {gonderen.display_name}, {unvan}",
        f"🔥🌋🔥 {gonderen.display_name}, {unvan}",
        f"🔥⚡🔥 {gonderen.display_name}, {unvan}",
        f"🌟🔥🌟 {gonderen.display_name}, 🔥 {unvan} 🔥"
    ]
    
    for effect in fire_effects:
        embed.set_footer(text=effect, icon_url=gonderen.avatar.url if gonderen.avatar else None)
        await message.edit(embed=embed)
        await asyncio.sleep(0.5)

async def simsek_animasyonu(message, embed, gonderen, unvan):
    """Şimşek efekti"""
    lightning_effects = [
        f"⚡ {gonderen.display_name}",
        f"⚡⚡ {gonderen.display_name}",
        f"⚡⚡⚡ {gonderen.display_name}, şarj oluyor...",
        f"🌩️ {gonderen.display_name}, {unvan}",
        f"⚡🌩️⚡ {gonderen.display_name}, {unvan}",
        f"🔋⚡🔋 {gonderen.display_name}, {unvan}",
        f"⚡👑⚡ {gonderen.display_name}, ⚡ {unvan} ⚡"
    ]
    
    for effect in lightning_effects:
        embed.set_footer(text=effect, icon_url=gonderen.avatar.url if gonderen.avatar else None)
        await message.edit(embed=embed)
        await asyncio.sleep(0.4)

async def yildiz_animasyonu(message, embed, gonderen, unvan):
    """Yıldız efekti"""
    star_effects = [
        f"⭐ {gonderen.display_name}",
        f"⭐⭐ {gonderen.display_name}",
        f"⭐⭐⭐ {gonderen.display_name}, parlıyor...",
        f"🌟 {gonderen.display_name}, {unvan}",
        f"⭐🌟⭐ {gonderen.display_name}, {unvan}",
        f"💫⭐💫 {gonderen.display_name}, {unvan}",
        f"🌟👑🌟 {gonderen.display_name}, 🌟 {unvan} 🌟"
    ]
    
    for effect in star_effects:
        embed.set_footer(text=effect, icon_url=gonderen.avatar.url if gonderen.avatar else None)
        await message.edit(embed=embed)
        await asyncio.sleep(0.6)

# SÜPER DUYURU KOMUTU
@bot.tree.command(name="duyuru", description="📢 Süper duyuru mesajı gönder")
@app_commands.describe(
    kanal="Duyuru kanalı",
    mesaj="Duyuru mesajı",
    gonderen="Duyuruyu yapan kişi",
    aciliyet="Duyuru aciliyet seviyesi"
)
@app_commands.choices(aciliyet=[
    app_commands.Choice(name="🟢 Normal", value="normal"),
    app_commands.Choice(name="🟡 Önemli", value="onemli"),
    app_commands.Choice(name="🔴 Acil", value="acil"),
    app_commands.Choice(name="🚨 Kritik", value="kritik")
])
@app_commands.default_permissions(administrator=True)
async def super_duyuru_komutu(
    interaction: discord.Interaction, 
    kanal: discord.TextChannel, 
    mesaj: str, 
    gonderen: discord.Member,
    aciliyet: str = "normal"
):
    # Aciliyet renkları
    aciliyet_map = {
        "normal": (0x00ff00, "🟢 NORMAL"),
        "onemli": (0xffff00, "🟡 ÖNEMLİ"),
        "acil": (0xff8000, "🟠 ACİL"),
        "kritik": (0xff0000, "🚨 KRİTİK")
    }
    
    color, aciliyet_text = aciliyet_map.get(aciliyet, (0x00ff00, "🟢 NORMAL"))
    
    embed = discord.Embed(
        title=f"📢 DUYURU - {aciliyet_text}",
        description=mesaj,
        color=color,
        timestamp=datetime.utcnow()
    )
    
    embed.set_author(
        name="🏛️ İTTİFAK ORDUSU | DUYURU SİSTEMİ",
        icon_url=bot.user.avatar.url if bot.user.avatar else None
    )
    
    embed.set_footer(
        text=f"👤 {gonderen.display_name} • 🛡️ Yetkilisi",
        icon_url=gonderen.avatar.url if gonderen.avatar else None
    )
    
    try:
        # @everyone mention sadece kritik durumlarda
        mention = "@everyone" if aciliyet == "kritik" else None
        
        await kanal.send(
            content=mention,
            embed=embed,
            allowed_mentions=discord.AllowedMentions(everyone=True) if mention else None
        )
        
        await interaction.response.send_message(
            f"✅ {aciliyet_text} duyuru {kanal.mention} kanalına gönderildi!", 
            ephemeral=True
        )
        
    except discord.Forbidden:
        await interaction.response.send_message("❌ Kanala mesaj göndermek için iznim yok!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Hata: {e}", ephemeral=True)

# ULTRA GELİŞMİŞ SİSTEM BİLGİSİ
@bot.tree.command(name="sistem-bilgi", description="🖥️ Detaylı sistem analizi ve performans raporu")
async def ultra_sistem_bilgi(interaction: discord.Interaction):
    try:
        await interaction.response.send_message("🔄 **Ultra sistem analizi başlatılıyor...**")
        
        import psutil
        import platform
        import sys
        
        # Bot bilgileri
        uptime = datetime.now() - bot.start_time
        uptime_str = str(uptime).split('.')[0]
        
        # Sistem bilgileri
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        ping = round(bot.latency * 1000)
        
        # Ana embed
        embed = discord.Embed(
            title="🖥️ ULTRA SİSTEM ANALİZİ",
            description="```ansi\n\u001b[1;36m▬▬▬▬▬▬ İTTİFAK ORDUSU SİSTEM RAPORU ▬▬▬▬▬▬\u001b[0m```",
            color=0x00ff41,
            timestamp=datetime.utcnow()
        )
        
        # Bot istatistikleri
        embed.add_field(
            name="🤖 **BOT İSTATİSTİKLERİ**",
            value=f"""
```yaml
🚀 Çalışma Süresi: {uptime_str}
🏓 Ping: {ping}ms
🏛️ Sunucular: {len(bot.guilds)}
👥 Kullanıcılar: {sum(g.member_count for g in bot.guilds):,}
⚡ Komutlar: {len(bot.tree.get_commands())}
🔧 Python: {sys.version.split()[0]}
📚 Discord.py: {discord.__version__}
```""",
            inline=False
        )
        
        # Sistem performansı
        def create_performance_bar(percentage, length=15):
            filled = int(length * percentage / 100)
            bar = "█" * filled + "░" * (length - filled)
            if percentage < 50:
                return f"🟢 `{bar}` {percentage}%"
            elif percentage < 80:
                return f"🟡 `{bar}` {percentage}%"
            else:
                return f"🔴 `{bar}` {percentage}%"
        
        embed.add_field(
            name="📊 **PERFORMANS ANALİZİ**",
            value=f"""
**💻 CPU Kullanımı:**
{create_performance_bar(cpu_percent)}

**🧠 RAM Kullanımı:**
{create_performance_bar(memory.percent)}
`{memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB`

**💾 Disk Kullanımı:**
{create_performance_bar(disk.percent)}
`{disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB`
""",
            inline=False
        )
        
        # Sistem durumu
        if cpu_percent < 50 and memory.percent < 70:
            status = "🟢 **MÜKEMMEL** - Sistem optimal performansta"
            embed.color = 0x00ff00
        elif cpu_percent < 80 and memory.percent < 85:
            status = "🟡 **İYİ** - Sistem normal çalışıyor"
            embed.color = 0xffff00
        else:
            status = "🔴 **DİKKAT** - Sistem yüksek yük altında"
            embed.color = 0xff0000
        
        embed.add_field(
            name="🎯 **SİSTEM DURUMU**",
            value=status,
            inline=False
        )
        
        # Platform bilgileri
        embed.add_field(
            name="🖥️ **PLATFORM BİLGİLERİ**",
            value=f"""
```yaml
İşletim Sistemi: {platform.system()} {platform.release()}
Mimari: {platform.machine()}
İşlemci: {platform.processor()[:50]}...
Ağ Durumu: ✅ Aktif
Güvenlik: 🛡️ Aktif
```""",
            inline=False
        )
        
        embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
        embed.set_footer(
            text=f"🔹 Rapor: {interaction.user.display_name} • 📊 Real-time Analysis",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )
        
        await interaction.edit_original_response(content=None, embed=embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Sistem Analizi Hatası",
            description=f"```{str(e)[:500]}```",
            color=0xff0000
        )
        await interaction.edit_original_response(content=None, embed=error_embed)

# SÜPER PİNG KOMUTU
@bot.tree.command(name="ping", description="🏓 Gelişmiş ping ve bağlantı kalitesi testi")
async def super_ping(interaction: discord.Interaction):
    start_time = time.time()
    
    await interaction.response.send_message("🏓 **Ping analizi yapılıyor...**")
    
    response_time = (time.time() - start_time) * 1000
    ws_ping = round(bot.latency * 1000)
    
    # Ping kalitesi analizi
    if ws_ping < 50:
        quality = "🟢 **MÜKEMMEL**"
        quality_desc = "Yıldırım hızında bağlantı!"
        color = 0x00ff00
    elif ws_ping < 100:
        quality = "🟡 **İYİ**"
        quality_desc = "Sorunsuz performans"
        color = 0xffff00
    elif ws_ping < 200:
        quality = "🟠 **ORTA**"
        quality_desc = "Kabul edilebilir gecikme"
        color = 0xff8000
    else:
        quality = "🔴 **YAVAŞ**"
        quality_desc = "Bağlantı problemleri olabilir"
        color = 0xff0000
    
    embed = discord.Embed(
        title="🏓 **PING ANALİZ RAPORU**",
        description=f"**Durum:** {quality_desc}",
        color=color,
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="⚡ **WebSocket Ping**",
        value=f"```{ws_ping}ms```",
        inline=True
    )
    
    embed.add_field(
        name="🔄 **API Response**",
        value=f"```{response_time:.0f}ms```",
        inline=True
    )
    
    embed.add_field(
        name="📊 **Kalite Değerlendirmesi**",
        value=quality,
        inline=True
    )
    
    # Ping çubuğu
    max_ping = 300
    ping_percentage = min(100, (ws_ping / max_ping) * 100)
    bar_length = 20
    filled = int(bar_length * (100 - ping_percentage) / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    embed.add_field(
        name="📈 **Performans Çubuğu**",
        value=f"`{bar}` **{100-ping_percentage:.0f}%**",
        inline=False
    )
    
    embed.set_footer(text=f"🔹 Test eden: {interaction.user.display_name}")
    
    await interaction.edit_original_response(content=None, embed=embed)

# QR KOD OLUŞTURUCU
@bot.tree.command(name="qr-kod", description="🔲 Gelişmiş QR kod oluşturucu")
@app_commands.describe(
    metin="QR koda dönüştürülecek metin",
    boyut="QR kod boyutu",
    stil="QR kod stili"
)
@app_commands.choices(boyut=[
    app_commands.Choice(name="📱 Küçük (200x200)", value="200"),
    app_commands.Choice(name="💻 Orta (400x400)", value="400"),
    app_commands.Choice(name="🖥️ Büyük (600x600)", value="600")
])
@app_commands.choices(stil=[
    app_commands.Choice(name="⚫ Klasik", value="klasik"),
    app_commands.Choice(name="🔵 Mavi", value="mavi"),
    app_commands.Choice(name="🔴 Kırmızı", value="kirmizi")
])
async def qr_kod_generator(
    interaction: discord.Interaction, 
    metin: str, 
    boyut: str = "400",
    stil: str = "klasik"
):
    if len(metin) > 1000:
        await interaction.response.send_message("❌ Metin çok uzun! Maksimum 1000 karakter.", ephemeral=True)
        return
    
    await interaction.response.send_message("🔲 **QR kod oluşturuluyor...**")
    
    try:
        # URL encode
        encoded_text = urllib.parse.quote(metin)
        
        # Stil renkleri
        color_map = {
            "klasik": "000000",
            "mavi": "0066cc",
            "kirmizi": "cc0000"
        }
        
        color = color_map.get(stil, "000000")
        
        # QR kod URL'si
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size={boyut}x{boyut}&data={encoded_text}&color={color}"
        
        embed = discord.Embed(
            title="🔲 **QR KOD OLUŞTURULDU**",
            description=f"**İçerik:** ```{metin[:200]}{'...' if len(metin) > 200 else ''}```",
            color=0x9932cc,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="📐 **Boyut**",
            value=f"`{boyut}x{boyut}px`",
            inline=True
        )
        
        embed.add_field(
            name="🎨 **Stil**",
            value=f"`{stil.title()}`",
            inline=True
        )
        
        embed.add_field(
            name="📊 **Karakter**",
            value=f"`{len(metin)}/1000`",
            inline=True
        )
        
        embed.set_image(url=qr_url)
        embed.set_footer(text=f"🔹 Oluşturan: {interaction.user.display_name}")
        
        await interaction.edit_original_response(content=None, embed=embed)
        
    except Exception as e:
        await interaction.edit_original_response(content=f"❌ QR kod oluşturma hatası: `{e}`")

# TEMIZLEME KOMUTU
@bot.tree.command(name="temizle", description="🧹 Gelişmiş mesaj temizleme sistemi")
@app_commands.describe(
    sayi="Silinecek mesaj sayısı (1-100)",
    kullanici="Belirli kullanıcının mesajlarını sil (opsiyonel)"
)
@app_commands.default_permissions(manage_messages=True)
async def temizle(interaction: discord.Interaction, sayi: int, kullanici: discord.Member = None):
    if sayi < 1 or sayi > 100:
        await interaction.response.send_message("❌ Mesaj sayısı 1-100 arasında olmalı!", ephemeral=True)
        return
    
    try:
        await interaction.response.send_message(f"🧹 Temizlik işlemi başlatılıyor...", ephemeral=True)
        
        if kullanici:
            # Belirli kullanıcının mesajlarını sil
            def check(message):
                return message.author == kullanici
            
            deleted = await interaction.channel.purge(limit=sayi*2, check=check)
            deleted_count = len(deleted)
            
            embed = discord.Embed(
                title="🧹 Temizlik Tamamlandı",
                description=f"✅ **{kullanici.mention}** kullanıcısının **{deleted_count}** mesajı silindi",
                color=0x00ff00
            )
        else:
            # Genel temizlik
            deleted = await interaction.channel.purge(limit=sayi)
            deleted_count = len(deleted)
            
            embed = discord.Embed(
                title="🧹 Temizlik Tamamlandı",
                description=f"✅ **{deleted_count}** mesaj silindi",
                color=0x00ff00
            )
        
        embed.set_footer(text=f"🔹 İşlem: {interaction.user.display_name}")
        
        # Geçici mesaj gönder
        temp_msg = await interaction.followup.send(embed=embed)
        
        # 5 saniye sonra sil
        await asyncio.sleep(5)
        await temp_msg.delete()
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Mesaj silmek için iznim yok!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Hata: {str(e)}", ephemeral=True)

# PREFIX KOMUTLARI
@bot.command(name='ping')
async def ping_prefix(ctx):
    ping = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! **{ping}ms**')

@bot.command(name='bilgi')
async def bilgi_prefix(ctx):
    embed = discord.Embed(
        title="🤖 Bot Bilgileri",
        description=f"**Sunucular:** {len(bot.guilds)}\n**Kullanıcılar:** {len(bot.users):,}",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

# MESAJ OLAYLARI
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Merhaba yanıtı
    if any(word in message.content.lower() for word in ['merhaba', 'selam', 'hello']):
        await message.channel.send(f'👋 Merhaba {message.author.mention}! Nasıl yardımcı olabilirim?')
    
    # Bot mention yanıtı
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        embed = discord.Embed(
            title="🤖 Merhaba!",
            description="Slash komutlarımı kullanarak benimle etkileşime geçebilirsin!\n`/` yazarak komutlarımı görebilirsin.",
            color=0x00ff00
        )
        await message.channel.send(embed=embed)
    
    await bot.process_commands(message)

# HATA YÖNETİMİ
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Bu komut bulunamadı! `/` yazarak slash komutlarımı görebilirsin.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu komutu kullanmak için yeterli yetkiye sahip değilsin!")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ Bu işlemi yapmak için gerekli izinlere sahip değilim!")
    else:
        print(f"Hata: {error}")

# BOT BAŞLATMA
if __name__ == "__main__":
    # Token kontrolü
    token = os.getenv('BOT_TOKEN')
    
    if token is None:
        print("❌ BOT_TOKEN environment variable bulunamadı!")
        print("💡 Railway'de BOT_TOKEN variable'ını eklediğinizden emin olun")
        print("🔧 Token formatı: MTM5MzY1NzA1...")
        exit(1)
    
    if len(token) < 50:
        print("❌ BOT_TOKEN çok kısa görünüyor!")
        print("💡 Doğru Discord bot token'ını kullandığınızdan emin olun")
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
