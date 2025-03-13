import discord
from discord.ext import commands
import os
import time
import sqlite3
from discord import ButtonStyle, Intents, Embed
from discord.ui import Button, View
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Помилка: Токен не знайдено. Переконайтеся, що .env файл містить DISCORD_BOT_TOKEN.")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)




@bot.event
async def on_ready():
    print(f'✅ Бот {bot.user.name} запущено!')

# 📋 Команда: Вакансії
@bot.command()
async def вакансії(ctx):
    embed = discord.Embed(
        title="📋 Доступні вакансії в RailTech",
        description="\n".join([
            "🚂 **Машиніст локомотива**",
            "👨‍🔧 **Помічник машиніста**",
            "📡 **Поїзний диспетчер**",
            "🛠️ **Локомотивна бригада**",
            "🚦 **Черговий по переїзду**",
            "🏢 **Черговий по станції**",
            "🔧 **Стрілочник**",
            "🚶 **Колійний обхідник**",
            "⚙️ **Механік**",
            "🎟️ **Кондуктор**"
        ]),
        color=discord.Color.green()
    )
    embed.set_footer(text="Обери свою професію та приєднуйся до RailTech!")
    await ctx.send(embed=embed)

# 📝 Команда: Анкета
@bot.command()
async def анкета(ctx):
    embed = Embed(title="📝 Анкета для вступу в RailTech", description="Заповніть анкету за посиланням нижче:", color=discord.Color.blue())
    embed.add_field(name="🔗 Посилання:", value="[Форма заявки](https://forms.gle/example)", inline=False)
    await ctx.send(embed=embed)

# 🛠️ Команда: Професія
@bot.command()
async def професія(ctx, *, job_name: str = None):
    JOB_DESCRIPTIONS = {
        "Машиніст локомотива": "Керує локомотивом та відповідає за безпеку руху.",
        "Помічник машиніста": "Допомагає машиністу в керуванні та перевіряє стан локомотива.",
        "Поїзний диспетчер": "Координує рух поїздів та контролює розклад.",
        "Локомотивна бригада": "Обслуговує та ремонтує локомотиви.",
        "Черговий по переїзду": "Стежить за безпекою на переїздах.",
        "Черговий по станції": "Контролює роботу станції та розклад відправлень.",
        "Стрілочник": "Керує стрілочними переводами на станції.",
        "Колійний обхідник": "Оглядає та обслуговує залізничні колії.",
        "Механік": "Виконує ремонт залізничного транспорту.",
        "Кондуктор": "Перевіряє квитки та допомагає пасажирам."
    }

    if job_name is None:
        embed = discord.Embed(title="📋 Доступні професії", color=discord.Color.green())
        for job, desc in JOB_DESCRIPTIONS.items():
            embed.add_field(name=f"🔹 {job}", value=desc, inline=False)
        await ctx.send(embed=embed)
    else:
        description = JOB_DESCRIPTIONS.get(job_name, "❌ Такої професії не знайдено. Спробуйте ще раз!")
        embed = discord.Embed(title=f"🛠️ {job_name}", description=description, color=discord.Color.orange())
        await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    await bot.process_commands(message)  # Обрабатывает команды правильно

@bot.command(name="хто_на_роботі")
async def хто_на_роботі(ctx):
    conn = sqlite3.connect("status.db")
    cursor = conn.cursor()

    # Отримуємо список користувачів зі статусом "На роботі"
    cursor.execute("SELECT username FROM users WHERE status = 'На роботі'")
    workers = [worker[0] for worker in cursor.fetchall()]
    conn.close()

    # Отримуємо список усіх учасників сервера з роллю "Працює"
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name="Працює")  # Виправлено помилку зі змінною
    if not role:
        await ctx.send("❌ Помилка: Роль **'Працює'** не знайдено!")
        return

    active_workers = [
        member.display_name for member in guild.members 
        if role in member.roles and member.name in workers
    ]

    # Формуємо Embed-відповідь
    if active_workers:
        worker_list = "\n".join(f"👷 {worker}" for worker in active_workers)
        embed = discord.Embed(
            title="🚂 Хто зараз на роботі?",
            description=worker_list,
            color=discord.Color.green()
        )
    else:
        embed = discord.Embed(
            title="⚠️ Наразі ніхто не працює!",
            description="Ніхто не вибрав статус **'На роботі'** або не має ролі **'Працює'**.",
            color=discord.Color.red()
        )

    await ctx.send(embed=embed)

# 📜 Команда: Правила
@bot.command()
async def правила(ctx):
    embed = discord.Embed(title="📌 Правила RailTech", description="Дотримуйтесь цих правил для кращої роботи компанії:", color=discord.Color.red())
    embed.add_field(name="1️⃣ Дисципліна", value="Заборонені образи та неадекватна поведінка.", inline=False)
    embed.add_field(name="2️⃣ Відповідальність", value="Кожен працівник повинен виконувати свої обов’язки.", inline=False)
    embed.add_field(name="3️⃣ Повага", value="Поважайте керівників та колег.", inline=False)
    embed.set_footer(text="RailTech - працюємо разом!")
    await ctx.send(embed=embed)

# 📌 Команда: Обрати статус
ROLE_MAPPING = {
    "✅На роботі": "Працює",
    "💤Відпочиває": "Відпочиває",
    "❌Не на роботі": "Неактивний"
}

@bot.command()
async def статус(ctx):
    view = View()
    statuses = ["✅На роботі", "💤Відпочиває", "❌Не на роботі"]

    async def button_callback(interaction: discord.Interaction):
        status = interaction.data['custom_id']
        role_name = ROLE_MAPPING.get(status)
        username = interaction.user.name

        # Оновлення статусу в базі
        conn = sqlite3.connect('status.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status = ? WHERE username = ?", (status, username))
        conn.commit()
        conn.close()

        # Видалення старої ролі та додавання нової
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        if member and role_name:
            for role in ROLE_MAPPING.values():
                existing_role = discord.utils.get(guild.roles, name=role)
                if existing_role in member.roles:
                    await member.remove_roles(existing_role)

            new_role = discord.utils.get(guild.roles, name=role_name)
            if new_role:
                await member.add_roles(new_role)

        await interaction.response.send_message(f"✅ Ваш статус змінено на {status}", ephemeral=True)

    for status in statuses:
        button = Button(label=status, style=discord.ButtonStyle.primary, custom_id=status)
        button.callback = button_callback
        view.add_item(button)

    await ctx.send("📌 **Оберіть свій статус:**", view=view)

# 📜 Команда: Надіслати
@bot.command()
@commands.has_permissions(administrator=True)  # Обмежуємо команду для адмінів
async def надіслати(ctx, канал: discord.TextChannel, *, повідомлення: str):
    """
    Надсилає повідомлення від імені бота в зазначений канал.
    Використання: !надіслати #назва-каналу Ваше повідомлення
    """
    try:
        await канал.send(повідомлення)
        await ctx.send(f"✅ Повідомлення успішно надіслано в {канал.mention}")
    except Exception as e:
        await ctx.send(f"❌ Помилка при надсиланні повідомлення: {e}")


# 📜 Команда: Всі доступні команди
@bot.command()
async def команди(ctx):
    embed = discord.Embed(title="📜 Список доступних команд", color=discord.Color.blue())
    commands_list = [
        ("📝 !анкета", "Отримати анкету для вступу в RailTech."),
        ("⚙️ !професія [назва]", "Дізнатися, за що відповідає певна професія."),
        ("📋 !вакансії", "Перелік всіх доступних вакансій у RailTech."),
        ("📜 !правила", "Переглянути основні правила RailTech."),
        ("🔧 !статус", "Обрати статус та отримати відповідну роль.")
    ]
    
    for name, desc in commands_list:
        embed.add_field(name=name, value=desc, inline=False)

    embed.set_footer(text="Використовуйте ці команди для взаємодії з ботом!")
    await ctx.send(embed=embed)



# Запуск бота
try:
    bot.run(TOKEN)
except Exception as e:
    print(f"❌ Помилка запуску бота: {e}")
    time.sleep(5)
