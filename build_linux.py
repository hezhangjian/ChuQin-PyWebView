#!/usr/bin/env python3
"""
Linux-specific build script for ChuQin PyWebView application.
"""

import sys
from build import main, Colors

if __name__ == "__main__":
    print(f"{Colors.WARNING}Building for Linux platform...{Colors.ENDC}")
    # Override sys.argv to pass --platform linux
    sys.argv = [sys.argv[0], "--platform", "linux"] + sys.argv[1:]
    main()
