import os
import hashlib
import time
import json
import sys

WATCH_DIR = "./monitored_files"
BASELINE_FILE = "baseline.json"

def calculate_sha256(filepath):
    """Calculates the SHA-256 cryptographic hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

def create_baseline():
    """Generates the initial cryptographic baseline of the directory."""
    baseline = {}
    print(f"[+] Scanning and generating baseline for: {WATCH_DIR}...")
    if not os.path.exists(WATCH_DIR):
        print(f"❌ Error: Target directory '{WATCH_DIR}' does not exist.")
        return
    for root, _, files in os.walk(WATCH_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_sha256(filepath)
            if file_hash:
                baseline[filepath] = file_hash
                print(f"  └─ Baselined: {filepath} ({file_hash[:10]}...)")
                
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)
    print(f"\n✅ Baseline successfully saved to '{BASELINE_FILE}' ({len(baseline)} files).")

def monitor():
    """Monitors the directory in real-time against the cryptographic baseline."""
    if not os.path.exists(BASELINE_FILE):
        print("❌ Error: Baseline file 'baseline.json' not found!")
        print("💡 Tip: Run 'python3 fim.py --init' first to generate your baseline.")
        return

    with open(BASELINE_FILE, "r") as f:
        baseline = json.load(f)

    print("\n" + "=" * 65)
    print("🛡️  CRYPTO FILE INTEGRITY MONITOR ACTIVE (Scanning every 2 seconds)")
    print("    Press Ctrl+C to safely exit the monitor.")
    print("=" * 65 + "\n")

    try:
        while True:
            current_files = {}
            for root, _, files in os.walk(WATCH_DIR):
                for file in files:
                    filepath = os.path.join(root, file)
                    file_hash = calculate_sha256(filepath)
                    if file_hash:
                        current_files[filepath] = file_hash

            for filepath, baseline_hash in baseline.copy().items():
                if filepath not in current_files:
                    print(f"🔴 ALERT: File DELETED! -> {filepath}")
                    del baseline[filepath]
                elif current_files[filepath] != baseline_hash:
                    print(f"🟡 ALERT: File MODIFIED! (Cryptographic Mismatch) -> {filepath}")
                    print(f"   ├─ Previous Hash: {baseline_hash[:16]}...")
                    print(f"   └─ New Hash: {current_files[filepath][:16]}...")
                    baseline[filepath] = current_files[filepath]

            for filepath, current_hash in current_files.items():
                if filepath not in baseline:
                    print(f"🟢 ALERT: New File Created! -> {filepath}")
                    print(f"   └─ File Hash: {current_hash[:16]}...")
                    baseline[filepath] = current_hash

            with open(BASELINE_FILE, "w") as f:
                json.dump(baseline, f, indent=4)

            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n[-] File Integrity Monitor stopped safely. Baseline updated on disk.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        create_baseline()
    else:
        monitor()