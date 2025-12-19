from typing import Optional
from tortoise import Tortoise
from dotenv import load_dotenv
import os
from urllib.parse import urlparse, parse_qs

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Debug: Print the DATABASE_URL (with password hidden)
if DATABASE_URL:
    parsed_debug = urlparse(DATABASE_URL)
    safe_url = f"{parsed_debug.scheme}://{parsed_debug.username}:****@{parsed_debug.hostname}:{parsed_debug.port or 5432}{parsed_debug.path}"
    print(f"🔍 DATABASE_URL found: {safe_url}")
else:
    print("❌ DATABASE_URL not found in environment variables!")
    print("💡 Make sure your .env file exists in the project root")
    raise RuntimeError("DATABASE_URL is not set")

# Parse the DATABASE_URL
parsed = urlparse(DATABASE_URL)

# Extract connection parameters
db_config = {
    "host": parsed.hostname,
    "port": parsed.port or 5432,
    "user": parsed.username,
    "password": parsed.password,
    "database": parsed.path.lstrip('/'),
    "ssl": "require"  # Neon requires SSL
}

# Debug: Print extracted config (with password hidden)
print(f"🔍 Extracted config:")
print(f"   Host: {db_config['host']}")
print(f"   Port: {db_config['port']}")
print(f"   User: {db_config['user']}")
print(f"   Database: {db_config['database']}")
print(f"   SSL: {db_config['ssl']}")

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": db_config
        }
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "UTC"
}


async def init_db():
    """Initialize database connection"""
    try:
        print("🔄 Initializing database connection...")
        await Tortoise.init(config=TORTOISE_ORM)
        print("🔄 Generating database schemas...")
        await Tortoise.generate_schemas()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise e


async def close_db():
    """Close database connection"""
    await Tortoise.close_connections()
    print("✅ Database connections closed")


# Test connection
async def test_db_connection():
    """Test database connection"""
    try:
        await init_db()
        print("✅ Database connection test successful")
        await close_db()
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        raise e


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_db_connection())