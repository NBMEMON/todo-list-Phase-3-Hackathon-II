from sqlmodel import SQLModel
from database.session import engine
from models.user import User
from models.task import Task
import sqlalchemy
from sqlalchemy import text

def recreate_tables_with_correct_schema():
    print("Recreating tables with correct schema...")
    
    # Connect to the database
    with engine.connect() as conn:
        # Drop the users table if it exists (using quoted identifier)
        try:
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            print("Dropped users table")
        except Exception as e:
            print(f"Error dropping users table: {e}")

        # Also try dropping with unquoted name in case
        try:
            conn.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
            print("Dropped user table (quoted)")
        except Exception as e:
            print(f"Error dropping user table (quoted): {e}")

        # Drop the task table if it exists
        try:
            conn.execute(text("DROP TABLE IF EXISTS task CASCADE"))
            print("Dropped task table")
        except Exception as e:
            print(f"Error dropping task table: {e}")

        # Commit the transaction
        conn.commit()
    
    # Recreate all tables based on models
    SQLModel.metadata.create_all(bind=engine)
    print("Tables recreated successfully!")
    
    # Verify the table structures
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"All tables in database: {tables}")

    if 'users' in tables:
        columns = inspector.get_columns('users')
        print(f"Columns in users table: {[col['name'] for col in columns]}")
    else:
        print("Users table was not created!")

    # Also check for 'user' table if it exists
    if 'user' in tables:
        columns = inspector.get_columns('user')
        print(f"Columns in user table: {[col['name'] for col in columns]}")

    # Check the task table structure
    if 'task' in tables:
        columns = inspector.get_columns('task')
        print(f"Columns in task table: {[col['name'] for col in columns]}")
    elif 'tasks' in tables:
        columns = inspector.get_columns('tasks')
        print(f"Columns in tasks table: {[col['name'] for col in columns]}")
    else:
        print("Task table was not created!")

if __name__ == "__main__":
    recreate_tables_with_correct_schema()