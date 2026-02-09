import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None, shell=False):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(
            cmd if not shell else cmd,
            cwd=cwd,
            shell=shell,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Success: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        raise e

def setup_and_push_to_hf_space(backend_dir, space_url, token):
    """Set up git repo in backend directory and push to Hugging Face Space."""
    
    # Convert to Path object
    backend_path = Path(backend_dir)
    
    # Initialize git repo if not exists
    if not (backend_path / '.git').exists():
        print(f"Initializing git repository in {backend_path}")
        run_command(['git', 'init'], cwd=backend_path)
        run_command(['git', 'checkout', '-b', 'main'], cwd=backend_path)
    
    # Add Hugging Face remote
    try:
        run_command(['git', 'remote', 'remove', 'hf'], cwd=backend_path)
    except:
        pass  # Remote might not exist yet
    
    # Format the remote URL with token (correct format for Hugging Face)
    hf_remote = f"https://user:{token}@huggingface.co/spaces/{space_url.split('/')[-2]}/{space_url.split('/')[-1]}"
    run_command(['git', 'remote', 'add', 'hf', hf_remote], cwd=backend_path)
    
    # Configure git user
    run_command(['git', 'config', 'user.name', 'FlowForge Assistant'], cwd=backend_path)
    run_command(['git', 'config', 'user.email', 'flowforge@example.com'], cwd=backend_path)
    
    # Add all files
    run_command(['git', 'add', '.'], cwd=backend_path)
    
    # Commit changes
    try:
        run_command(['git', 'commit', '-m', 'Initial commit: Hackathon Phase 3 Backend'], cwd=backend_path)
    except subprocess.CalledProcessError:
        print("No changes to commit or commit failed, continuing...")
        pass  # May not have changes to commit
    
    # Push to Hugging Face Space
    print("Pushing to Hugging Face Space...")
    run_command(['git', 'push', '-u', 'hf', 'main', '--force'], cwd=backend_path)
    
    print(f"Successfully pushed backend to {space_url}")

if __name__ == "__main__":
    # Define paths and credentials
    BACKEND_DIR = r"E:\Hackathon-Todo List Phase III\backend"
    SPACE_URL = "https://huggingface.co/spaces/Naeeb/hackathon_phase_3_1"
    ACCESS_TOKEN = os.getenv("HF_TOKEN")
    if not ACCESS_TOKEN:
        print("Error: HF_TOKEN environment variable not set")
        sys.exit(1)
    
    # Call the function to push to HF Space
    setup_and_push_to_hf_space(BACKEND_DIR, SPACE_URL, ACCESS_TOKEN)