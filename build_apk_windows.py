#!/usr/bin/env python3
"""
Quick APK Builder for Windows
Alternative to Buildozer - uses python-for-android directly
"""

import os
import sys
import subprocess

def run_command(cmd):
    """Run shell command and return output"""
    print(f"\n▶ Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"⚠️ {result.stderr}")
    return result.returncode == 0

def build_apk():
    """Build APK using python-for-android"""
    
    print("=" * 60)
    print("  📱 Medicine Reminder - APK Builder")
    print("=" * 60)
    
    # Check if p4a is installed
    print("\n[1/5] Checking python-for-android...")
    try:
        import pythonforandroid
        print("✅ python-for-android installed")
    except ImportError:
        print("Installing python-for-android...")
        if not run_command("pip install python-for-android"):
            print("❌ Failed to install python-for-android")
            return False
    
    # Set up environment
    print("\n[2/5] Setting up build environment...")
    os.chdir(r"d:\capston-project")
    
    # Create APK build command
    print("\n[3/5] Preparing APK build...")
    
    apk_cmd = [
        "p4a",
        "apk",
        "--private", ".",
        "--package", "org.medicinereminder.app",
        "--name", "MedicineReminder",
        "--version", "1.0",
        "--bootstrap", "sdl2",
        "--requirements", "python3,kivy,kivymd,pandas",
        "--permission", "INTERNET,WRITE_EXTERNAL_STORAGE,VIBRATE",
        "--orientation", "portrait",
        "--icon", "app_icon.png",  # Optional
    ]
    
    print("\n[4/5] Building APK...")
    print("⏱️  This may take 30-60 minutes on first run...")
    print("☕ Please wait...")
    
    cmd = " ".join(apk_cmd)
    if run_command(cmd):
        print("\n[5/5] ✅ APK Build Complete!")
        print("\n📁 APK Location: Check current directory")
        return True
    else:
        print("\n❌ APK Build Failed")
        print("\nℹ️  Note: Building APK on Windows requires:")
        print("   - Android SDK/NDK")
        print("   - Java JDK")
        print("   - Proper environment variables")
        print("\n💡 Recommended: Use WSL2 with buildozer instead")
        return False

if __name__ == "__main__":
    print("\n⚠️  WARNING: Building APK directly on Windows is complex")
    print("This requires Android SDK, NDK, and Java to be installed")
    print("\n✅ RECOMMENDED: Wait for WSL Ubuntu to finish installing")
    print("   Then use: buildozer android debug")
    print("\nDo you want to continue? (y/n): ", end="")
    
    # For automated run, skip prompt
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        choice = "n"
    else:
        choice = input().lower()
    
    if choice == 'y':
        build_apk()
    else:
        print("\n✅ Good choice! WSL method is much easier.")
        print("\nTo build APK with WSL:")
        print("1. Wait for Ubuntu installation to complete")
        print("2. Open Ubuntu terminal")
        print("3. Run: cd /mnt/d/capston-project")
        print("4. Run: bash build_apk_wsl.sh")
        print("5. Run: buildozer android debug")
