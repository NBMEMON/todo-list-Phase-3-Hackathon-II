import sys
import os

# Add the backend directory to the path to resolve relative imports correctly
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

try:
    from utils.jwt import verify_access_token
    print("Successfully imported from local utils.jwt")
except ImportError as e:
    print(f"Failed to import from local utils.jwt: {e}")

try:
    import main
    print("Successfully imported main module")
except ImportError as e:
    print(f"Failed to import main: {e}")