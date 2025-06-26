#!/usr/bin/env python3
"""
Security Policy Generator - Startup Script
"""

import os
import sys
from app import app

def main():
    """Main function to start the application"""
    print("=" * 60)
    print("🔒 Security Policy Generator")
    print("=" * 60)
    print("Generating comprehensive security policies based on compliance frameworks")
    print("Supported frameworks: ISO 27001, ISO 42001, PCI DSS, SOC 2, GDPR")
    print("=" * 60)
    
    # Create temp directory if it doesn't exist
    os.makedirs('temp', exist_ok=True)
    
    # Set default port
    port = int(os.environ.get('PORT', 5000))
    
    # Set debug mode based on environment
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting application on http://localhost:{port}")
    print(f"📝 Debug mode: {'Enabled' if debug else 'Disabled'}")
    print("=" * 60)
    print("Press Ctrl+C to stop the application")
    print("=" * 60)
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            use_reloader=debug
        )
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 