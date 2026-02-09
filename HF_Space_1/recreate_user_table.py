import asyncio
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from database.session import engine
from models.user import User

def recreate_user_table():
    print("Dropping and recreating user table with correct schema...")
    
    # Connect to the database
    with engine.connect() as conn:
        # Drop the user table if it exists
        try:
            conn.execute(text("DROP TABLE IF EXISTS user CASCADE"))
            print("Dropped user table")
        except Exception as e:
            print(f"Error dropping user table: {e}")
        
        # Commit the transaction
        conn.commit()
    
    # Recreate all tables based on models
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)
    print("Tables recreated successfully!")
    
    # Verify the user table structure
    from sqlalchemy import inspect
    inspector = inspect(engine)
    if 'user' in inspector.get_table_names():
        columns = inspector.get_columns('user')
        print(f"Columns in recreated user table: {[col['name'] for col in columns]}")
    else:
        print("User table was not created!")

if __name__ == "__main__":
    recreate_user_table()