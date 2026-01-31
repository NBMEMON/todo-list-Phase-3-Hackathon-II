from sqlmodel import SQLModel
from database.session import engine
from models.user import User
from models.task import Task

print("Creating database tables...")
try:
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # Verify tables exist
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")
    
    if 'user' in tables:
        columns = inspector.get_columns('user')
        print(f"Columns in user table: {[col['name'] for col in columns]}")
    else:
        print("User table does not exist!")
        
except Exception as e:
    print(f"Error creating tables: {e}")