#!/usr/bin/env python3
"""
Claude API Setup Script
This script helps you set up your Claude API key for the security policy generator.
"""

import os
import sys

def main():
    print("🔧 Claude API Setup for Security Policy Generator")
    print("=" * 50)
    
    # Check if API key is already set
    current_key = os.environ.get('CLAUDE_API_KEY')
    if current_key and current_key != 'sk-ant-your-api-key-here':
        print(f"✅ Claude API key is already set: {current_key[:10]}...")
        print("The app should work with Claude features enabled.")
        return
    
    print("❌ Claude API key not found or not set properly.")
    print("\nTo enable Claude AI features, you need to:")
    print("\n1. Get your API key from https://console.anthropic.com/")
    print("2. Set the environment variable using one of these methods:")
    
    print("\n📝 Method 1: Set for current session")
    print("export CLAUDE_API_KEY='sk-ant-your-actual-api-key'")
    
    print("\n📝 Method 2: Add to your shell profile (~/.zshrc, ~/.bashrc, etc.)")
    print("echo \"export CLAUDE_API_KEY='sk-ant-your-actual-api-key'\" >> ~/.zshrc")
    print("source ~/.zshrc")
    
    print("\n📝 Method 3: Set in the app directly")
    print("Edit app.py and change line:")
    print("claude_generator = ClaudePolicyGenerator(api_key='sk-ant-your-actual-api-key')")
    
    print("\n🔍 Current status:")
    if current_key:
        print(f"   API Key: {current_key}")
    else:
        print("   API Key: Not set")
    
    print("\n📖 For more details, see CLAUDE_SETUP.md")
    
    # Ask if user wants to set it now
    try:
        response = input("\nWould you like to set the API key now? (y/n): ").lower().strip()
        if response == 'y':
            api_key = input("Enter your Claude API key (starts with sk-ant-): ").strip()
            if api_key.startswith('sk-ant-'):
                print(f"\n✅ Setting API key: {api_key[:10]}...")
                os.environ['CLAUDE_API_KEY'] = api_key
                print("API key set for current session. Restart the app to use Claude features.")
            else:
                print("❌ Invalid API key format. Should start with 'sk-ant-'")
        else:
            print("You can set the API key later and restart the app.")
    except KeyboardInterrupt:
        print("\nSetup cancelled.")
        return

if __name__ == "__main__":
    main() 