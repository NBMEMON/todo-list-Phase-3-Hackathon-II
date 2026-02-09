import os

print("Starting upload to Hugging Face Space...")
token = os.getenv('HF_TOKEN')
if not token:
    raise ValueError("HF_TOKEN environment variable not set")
api = HfApi(token=token)

api.upload_folder(
    folder_path='HF_Space',
    repo_id='Naeeb/hackathon_phase_3_1',
    repo_type='space',
    path_in_repo='.',
    ignore_patterns=['.git', '.env', '__pycache__', '*tmp*', '*.log'],
    commit_message='Deploy backend code'
)

print("Upload successfully completed!")
