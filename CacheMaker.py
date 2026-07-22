################# By Nazky  ##############
import os
from datetime import datetime

# Configuration
EXCLUDED_DIRS = {'.venv', '.git', 'noneed', '.github', 'node_modules'}
EXCLUDED_EXTENSIONS = {
    '.bat', '.txt', '.exe', '.mp4', '.py', '.bak', '.zip',
    '.mp3', '.sh', '.h', '.c', '.o', '.ld', '.md', '.d', '.json'
}
EXCLUDED_FILES = {'.gitignore', '.htaccess', 'COPYING', 'LICENSE', 'MAKEFILE', 'dockerfile', '.gitinclude', '.prettierrc', '.keepgithub'}
OUTPUT_FILE = 'PSFree.manifest'

def create_manifest():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(root_dir, OUTPUT_FILE)
    with open(manifest_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write("CACHE MANIFEST\n")
        f.write(f"# v1\n")
        f.write(f"# Generated on {datetime.now().isoformat()}\n\n")
        f.write("CACHE:\n")
        # Walk through all files
        cached_files = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Remove excluded directories (modifies the dirnames list in-place)
            dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS)
            for filename in sorted(filenames):
                filepath = os.path.join(dirpath, filename)
                relpath = os.path.relpath(filepath, root_dir)
                # Skip excluded files, extensions and the manifest file itself
                ext = os.path.splitext(filename)[1].lower()
                if (ext in EXCLUDED_EXTENSIONS or
                    filename in EXCLUDED_FILES or
                    filename == OUTPUT_FILE):
                    continue
                cached_files.append(relpath.replace(os.sep, '/'))

        for relpath in sorted(cached_files):
            full_path = os.path.join(root_dir, relpath.replace('/', os.sep))
            if not os.path.isfile(full_path):
                raise FileNotFoundError(f"Cache entry does not exist: {relpath}")
            f.write(f"{relpath}\n")
        # Write network section
        f.write("\nNETWORK:\n")
        f.write("*\n")

    print(f"Successfully created {OUTPUT_FILE}")
    print(f"Cached files: {len(cached_files)}")
    print(f"Excluded folders: {', '.join(EXCLUDED_DIRS)}")

if __name__ == "__main__":
    create_manifest()
