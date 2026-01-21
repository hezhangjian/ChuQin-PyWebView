#!/usr/bin/env python3
"""
macOS-specific build script for ChuQin PyWebView application.
"""

import sys
from build import main, Colors

if __name__ == "__main__":
    print(f"{Colors.WARNING}Building for macOS platform...{Colors.ENDC}")
    # Override sys.argv to pass --platform darwin
    sys.argv = [sys.argv[0], "--platform", "darwin"] + sys.argv[1:]
    main()
