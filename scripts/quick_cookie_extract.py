#!/usr/bin/env python3
"""
Quick Cookie Extractor - Extracts YouTube cookies when Chrome is closed
Run this script, then close Chrome when prompted, and cookies will be extracted automatically.
"""

import os
import sys
import time
import shutil
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime

def check_chrome_running():
    """Check if Chrome is running"""
    import subprocess
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq chrome.exe'],
                              capture_output=True, text=True)
        return 'chrome.exe' in result.stdout.lower()
    except:
        return False

def extract_cookies():
    """Extract cookies from Chrome Profile 1"""
    cookie_path = Path.home() / 'AppData' / 'Local' / 'Google' / 'Chrome' / 'User Data' / 'Profile 1' / 'Network' / 'Cookies'

    if not cookie_path.exists():
        print(f"[ERROR] Cookie database not found: {cookie_path}")
        return False

    try:
        # Copy database
        temp_file = tempfile.mktemp(suffix='.db')
        shutil.copy2(cookie_path, temp_file)
        print(f"[OK] Copied cookie database")

        # Read cookies
        conn = sqlite3.connect(temp_file)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT host_key, path, is_secure, expires_utc, name, value
            FROM cookies
            WHERE (host_key LIKE '%youtube%' OR host_key LIKE '%.google.com') AND value != ''
        """)

        rows = cursor.fetchall()
        print(f"[OK] Found {len(rows)} YouTube/Google cookies")

        if rows:
            # Save to cookies.txt
            with open("cookies.txt", 'w', encoding='utf-8') as f:
                f.write("# Netscape HTTP Cookie File\n")
                f.write(f"# Generated on {datetime.now().isoformat()}\n")
                f.write("# From Chrome Profile 1\n\n")

                for row in rows:
                    host_key, path, is_secure, expires_utc, name, value = row
                    secure = "TRUE" if is_secure else "FALSE"
                    expiry = (expires_utc - 11644473600000000) // 1000000 if expires_utc > 0 else 0
                    f.write(f"{host_key}\tTRUE\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")

            print(f"[OK] Saved to cookies.txt ({os.path.getsize('cookies.txt')} bytes)")

            # Preview
            print("\n[PREVIEW] First 5 cookies:")
            for row in rows[:5]:
                print(f"  {row[0]}: {row[4]}")

            conn.close()
            os.unlink(temp_file)
            return True
        else:
            print("[WARN] No cookies found with values")
            conn.close()
            os.unlink(temp_file)
            return False

    except PermissionError:
        print("[ERROR] Chrome is still running. Please close it completely.")
        return False
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return False

def main():
    print("=" * 60)
    print("Quick Cookie Extractor for YouTube")
    print("=" * 60)

    # Check if Chrome is running
    if check_chrome_running():
        print("\n[WARN] Chrome is currently running.")
        print("[INFO] Please close ALL Chrome windows, then press Enter...")
        input()

        # Wait a moment for Chrome to fully close
        print("[INFO] Waiting for Chrome to close completely...")
        time.sleep(2)

        # Check again
        if check_chrome_running():
            print("[ERROR] Chrome is still running. Please close it completely and try again.")
            return 1

    print("\n[INFO] Extracting cookies...")
    if extract_cookies():
        print("\n" + "=" * 60)
        print("[SUCCESS] Cookies extracted successfully!")
        print("=" * 60)
        print("\nYou can now run:")
        print('  python process_video.py --url "https://www.youtube.com/watch?v=a9eR1xsfvHg" --language zh --save-to-file')
        print("\nYou can also reopen Chrome now.")
        return 0
    else:
        print("\n[FAILED] Could not extract cookies.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
