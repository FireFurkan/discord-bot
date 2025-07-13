import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from datetime import datetime

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot başlangıç zamanı
start_time = datetime.now()

@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} olarak giriş yaptı!')
    print(f'📊 {len(bot.guilds)} sunucuda aktif')
    
    # Slash komutları senkronize et
    try:
        synced = await bot.tree.sync()
        print(f'✅ {len(synced)} slash komutu senkronize edildi')
    except Exception as e:
        print(f'❌ Slash komut hatası: {e}')
    
    # Bot durumu ayarla
    await bot.change_presence(
        activity=discord.Game(name="🤖 7/24 Aktif Bot"),
        status=discord.Status.online
    )

# Slash Komut: /ping
@bot.tree.command(name="ping", description="Bot gecikme süresini gösterir")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"**Gecikme:** `{latency}ms`",
        color=0x00ff00 if latency < 100 else 0xffff00
    )
    
    await interaction.response.send_message(embed=embed)

# Slash Komut: /bilgi
@bot.tree.command(name="bilgi", description="Bot hakkında bilgi verir")
async def bilgi(interaction: discord.Interaction):
    uptime = datetime.now() - start_time
    uptime_str = str(uptime).split('.')[0]
    
    embed = discord.Embed(
        title="🤖 Bot Bilgileri",
        color=0x0099ff
    )
    
    embed.add_field(name="📊 Sunucular", value=len(bot.guilds), inline=True)
    embed.add_field(name="👥 Kullanıcılar", value=len(bot.users), inline=True)
    embed.add_field(name="⏰ Uptime", value=uptime_str, inline=True)
    embed.add_field(name="🏓 Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)
    
    embed.set_footer(text=f"İsteyen: {interaction.user.display_name}")
    
    await interaction.response.send_message(embed=embed)

# Slash Komut: /mesaj
@bot.tree.command(name="mesaj", description="Belirtilen kanala mesaj gönderir")
@app_commands.describe(
    kanal="Mesajın gönderileceği kanal",
    icerik="Gönderilecek mesaj içeriği"
)
@app_commands.default_permissions(administrator=True)
async def mesaj(interaction: discord.Interaction, kanal: discord.TextChannel, icerik: str):
    try:
        embed = discord.Embed(
            description=icerik,
            color=0x1e90ff,
            timestamp=datetime.now()
        )
        
        embed.set_author(
            name="Bot Mesajı",
            icon_url=bot.user.avatar.url if bot.user.avatar else None
        )
        
        embed.set_footer(
            text=f"Gönderen: {interaction.user.display_name}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else None
        )
        
        await kanal.send(embed=embed)
        await interaction.response.send_message(
            f"✅ Mesaj {kanal.mention} kanalına gönderildi!", 
            ephemeral=True
        )
        
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Bu kanala mesaj göndermek için iznim yok!", 
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Hata: {str(e)}", 
            ephemeral=True
        )

# Slash Komut: /temizle
@bot.tree.command(name="temizle", description="Belirtilen sayıda mesajı siler")
@app_commands.describe(sayi="Silinecek mesaj sayısı (1-100)")
@app_commands.default_permissions(manage_messages=True)
async def temizle(interaction: discord.Interaction, sayi: int):
    if sayi < 1 or sayi > 100:
        await interaction.response.send_message(
            "❌ Mesaj sayısı 1-100 arasında olmalı!", 
            ephemeral=True
        )
        return
    
    try:
        deleted = await interaction.channel.purge(limit=sayi)
        await interaction.response.send_message(
            f"✅ {len(deleted)} mesaj silindi!", 
            ephemeral=True
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Mesaj silmek için iznim yok!", 
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Hata: {str(e)}", 
            ephemeral=True
        )

# Prefix Komutlar
@bot.command(name='ping')
async def ping_prefix(ctx):
    await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms')

@bot.command(name='bilgi')
async def bilgi_prefix(ctx):
    embed = discord.Embed(
        title="Bot Bilgileri",
        description=f"**Sunucular:** {len(bot.guilds)}\n**Kullanıcılar:** {len(bot.users)}",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

# Mesaj olayları
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Merhaba yanıtı
    if 'merhaba' in message.content.lower():
        await message.channel.send(f'Merhaba {message.author.mention}! 👋')
    
    # Komutları işle
    await bot.process_commands(message)

# Hata yönetimi
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Bu komut bulunamadı!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu komutu kullanmak için yetkiniz yok!")
    else:
        await ctx.send(f"❌ Bir hata oluştu: {str(error)}")

# Bot çalıştırma
if __name__ == "__main__":
    # Token'ı environment variable'dan al
    token = os.getenv('BOT_TOKEN')
    
    if token is None:
        print("❌ BOT_TOKEN environment variable bulunamadı!")
        print("💡 Railway'de BOT_TOKEN variable'ını eklediğinizden emin olun")
        exit(1)
    
    try:
        print("🚀 Bot başlatılıyor...")
        bot.run(token)
    except discord.LoginFailure:
        print("❌ Bot token'ı geçersiz!")
    except Exception as e:
        print(f"❌ Bot başlatılamadı: {e}")
