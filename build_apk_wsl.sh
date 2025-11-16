#!/bin/bash

# Medicine Reminder APK Build Script for WSL2
# Run this script in Ubuntu WSL terminal

echo "🚀 Medicine Reminder APK Builder"
echo "=================================="
echo ""

# Check if running in WSL
if ! grep -qi microsoft /proc/version; then
    echo "❌ This script must be run in WSL (Windows Subsystem for Linux)"
    exit 1
fi

echo "📦 Step 1: Installing system dependencies..."
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    git \
    zip \
    unzip \
    openjdk-11-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev

echo ""
echo "🐍 Step 2: Installing Python packages..."
pip3 install --upgrade pip
pip3 install --upgrade cython
pip3 install buildozer

echo ""
echo "📂 Step 3: Navigating to project directory..."
cd /mnt/d/capston-project || {
    echo "❌ Project directory not found!"
    echo "Please ensure your project is at d:\\capston-project"
    exit 1
}

echo ""
echo "✅ Setup complete!"
echo ""
echo "📱 To build APK, run:"
echo "   buildozer android debug"
echo ""
echo "⏱️  First build may take 30-60 minutes"
echo "📍 APK will be saved in: bin/ folder"
echo ""
