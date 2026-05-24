import aiosqlite

DB_PATH = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                coins INTEGER DEFAULT 0,
                warns INTEGER DEFAULT 0,
                is_vip INTEGER DEFAULT 0,
                daily_last INTEGER DEFAULT 0,
                messages INTEGER DEFAULT 0,
                is_banned INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS warns_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                chat_id INTEGER,
                admin_id INTEGER,
                reason TEXT,
                created_at INTEGER DEFAULT (strftime('%s','now'))
            );
            CREATE TABLE IF NOT EXISTS game_stats (
                user_id INTEGER PRIMARY KEY,
                dice_wins INTEGER DEFAULT 0,
                dice_games INTEGER DEFAULT 0,
                slot_wins INTEGER DEFAULT 0,
                slot_games INTEGER DEFAULT 0
            );
        """)
        await db.commit()
    print("✅ БД готова")
