from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Updating database schema...")
    
    # Add sex column
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS sex VARCHAR(10)"))
            conn.commit()
        print("✅ Added 'sex' column to users table")
    except Exception as e:
        print(f"⚠️  Could not add 'sex' column: {e}")

    # Create user_favorites table
    try:
        with db.engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_favorites (
                    user_id VARCHAR(36) NOT NULL,
                    place_id VARCHAR(36) NOT NULL,
                    PRIMARY KEY (user_id, place_id),
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (place_id) REFERENCES places (id)
                )
            """))
            conn.commit()
            print("✅ Created 'user_favorites' table")
    except Exception as e:
        print(f"❌ Failed to create 'user_favorites' table: {e}")

print("Database update complete.")
