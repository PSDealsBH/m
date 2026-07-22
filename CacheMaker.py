################# By Nazky ##############
import hashlib
import os

OUTPUT_FILE = "PSFree.manifest"

# Minimal PS4 9.00 / GoldHEN offline runtime. Keep this explicit so hidden
# payloads, other firmware files, and development files never enter AppCache.
REQUIRED_FILES = [
    "cache.html",
    "exploit.html",
    "index.html",
    "includes/css/colors/default.css",
    "includes/css/colors/vibrant.css",
    "includes/css/layouts/compact.css",
    "includes/css/layouts/index.css",
    "includes/css/ps-deals-bh.css",
    "includes/images/instagram-qr.jpeg",
    "includes/images/ps-deals-bg.png",
    "includes/js/HENs.js",
    "includes/js/autoJbRetry.js",
    "includes/js/checkFw.js",
    "includes/js/design.js",
    "includes/js/events.js",
    "includes/js/exploits/bundle.js",
    "includes/js/index-legacy.js",
    "includes/js/index.js",
    "includes/js/language.js",
    "includes/js/languages/ar.js",
    "includes/js/languages/en.js",
    "includes/js/languages/es.js",
    "includes/js/languages/fa.js",
    "includes/js/languages/ru.js",
    "includes/js/languages/tr.js",
    "includes/js/languages/zh-cn.js",
    "includes/js/payloadsList.js",
    "includes/payloads/GoldHEN/goldhen_v2.4b18.10.bin",
    "includes/payloads/payloads.js",
    "src/fonts/LiberationMono-Regular.ttf",
]


def create_manifest():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(root_dir, OUTPUT_FILE)
    revision_hash = hashlib.sha256()

    for relpath in REQUIRED_FILES:
        full_path = os.path.join(root_dir, relpath.replace("/", os.sep))
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Required cache file does not exist: {relpath}")
        revision_hash.update(relpath.encode("utf-8"))
        with open(full_path, "rb") as cached_file:
            for chunk in iter(lambda: cached_file.read(65536), b""):
                revision_hash.update(chunk)

    revision = revision_hash.hexdigest()[:16]
    content = [
        "CACHE MANIFEST",
        "# PS_DEALS_BH Offline Cache",
        f"# revision: {revision}",
        "",
        "CACHE:",
        *REQUIRED_FILES,
        "",
        "NETWORK:",
        "*",
        "",
    ]
    new_manifest = "\n".join(content)

    old_manifest = ""
    if os.path.isfile(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as manifest_file:
            old_manifest = manifest_file.read()

    if new_manifest != old_manifest:
        with open(manifest_path, "w", encoding="utf-8", newline="\n") as manifest_file:
            manifest_file.write(new_manifest)
        print(f"Updated {OUTPUT_FILE} (revision {revision})")
    else:
        print(f"No changes to {OUTPUT_FILE} (revision {revision})")

    print(f"Cached files: {len(REQUIRED_FILES)}")


if __name__ == "__main__":
    create_manifest()
