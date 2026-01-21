#!/usr/bin/env python3
"""
Windows-specific build script for ChuQin PyWebView application.
"""

import sys
from build import main, Colors

if __name__ == "__main__":
    print(f"{Colors.WARNING}Building for Windows platform...{Colors.ENDC}")
    # Override sys.argv to pass --platform windows
    sys.argv = [sys.argv[0], "--platform", "windows"] + sys.argv[1:]
    main()
