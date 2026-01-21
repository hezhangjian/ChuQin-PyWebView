#!/usr/bin/env python3
"""
Unified build script for ChuQin PyWebView application.
Supports building for Windows, macOS, and Linux platforms.
"""

import sys
import subprocess
import shutil
import platform
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_info(msg):
    print(f"{Colors.OKBLUE}[INFO]{Colors.ENDC} {msg}")


def print_success(msg):
    print(f"{Colors.OKGREEN}[SUCCESS]{Colors.ENDC} {msg}")


def print_warning(msg):
    print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} {msg}")


def print_error(msg):
    print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {msg}")


def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.absolute()


def check_dependencies():
    """Check if required dependencies are installed"""
    print_info("Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print_error("Python 3.9 or higher is required")
        return False
    
    # Check PyInstaller
    try:
        import PyInstaller
        print_success(f"PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print_error("PyInstaller not found. Install with: pip install pyinstaller")
        return False
    
    # Check Node.js and package manager
    portal_dir = get_project_root() / "portal"
    node_modules = portal_dir / "node_modules"
    
    if not node_modules.exists():
        print_warning("Frontend dependencies not installed")
        print_info("Installing frontend dependencies...")
        if not install_frontend_deps(portal_dir):
            return False
    
    return True


def install_frontend_deps(portal_dir):
    """Install frontend dependencies"""
    lock_file = portal_dir / "pnpm-lock.yaml"
    
    # Check for pnpm
    if lock_file.exists():
        if shutil.which("pnpm"):
            cmd = ["pnpm", "install"]
        else:
            print_error("pnpm not found. Please install pnpm: npm install -g pnpm")
            return False
    else:
        if shutil.which("npm"):
            cmd = ["npm", "install"]
        else:
            print_error("npm not found. Please install Node.js")
            return False
    
    try:
        subprocess.run(cmd, cwd=str(portal_dir), check=True)
        print_success("Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install frontend dependencies")
        return False


def build_frontend():
    """Build the frontend application"""
    print_info("Building frontend...")
    portal_dir = get_project_root() / "portal"
    dist_dir = portal_dir / "dist"
    
    # Remove old dist if exists
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # Determine package manager
    lock_file = portal_dir / "pnpm-lock.yaml"
    if lock_file.exists():
        cmd = ["pnpm", "build"]
    else:
        cmd = ["npm", "run", "build"]
    
    try:
        subprocess.run(cmd, cwd=str(portal_dir), check=True)
        
        # Verify build output
        index_html = dist_dir / "index.html"
        if not index_html.exists():
            print_error("Frontend build failed: index.html not found")
            return False
        
        print_success("Frontend built successfully")
        return True
    except subprocess.CalledProcessError:
        print_error("Frontend build failed")
        return False


def build_app(target_platform=None):
    """Build the application using PyInstaller"""
    project_root = get_project_root()
    
    # Determine target platform
    if target_platform is None:
        target_platform = platform.system().lower()
    
    print_info(f"Building for platform: {target_platform}")
    
    # Build with PyInstaller
    spec_file = project_root / "chuqin.spec"
    if not spec_file.exists():
        print_error(f"Spec file not found: {spec_file}")
        print_info("Please run 'python build.py --init' first to generate spec file")
        return False
    
    try:
        cmd = [
            sys.executable,
            "-m", "PyInstaller",
            str(spec_file),
            "--clean",
            "--noconfirm"
        ]
        
        # Note: When using a .spec file, windowed/console options are set in the spec file itself
        # (see console=False in chuqin.spec). Do not add --windowed/--console flags here.
        
        # Run PyInstaller from project root to ensure correct path resolution
        subprocess.run(cmd, check=True, cwd=str(project_root))
        print_success("Application built successfully")
        
        # Show output location
        if target_platform == "windows":
            exe_path = project_root / "dist" / "ChuQin.exe"
            if exe_path.exists():
                print_success(f"Executable: {exe_path}")
        elif target_platform == "darwin":
            app_path = project_root / "dist" / "ChuQin.app"
            if app_path.exists():
                print_success(f"Application: {app_path}")
        else:
            exe_path = project_root / "dist" / "ChuQin"
            if exe_path.exists():
                print_success(f"Executable: {exe_path}")
        
        return True
    except subprocess.CalledProcessError:
        print_error("Build failed")
        return False


def main():
    """Main build function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Build ChuQin PyWebView application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build.py                    # Build for current platform
  python build.py --platform windows # Build for Windows
  python build.py --platform darwin  # Build for macOS
  python build.py --platform linux   # Build for Linux
        """
    )
    
    parser.add_argument(
        "--platform",
        choices=["windows", "darwin", "linux"],
        help="Target platform (default: current platform)"
    )
    parser.add_argument(
        "--skip-frontend",
        action="store_true",
        help="Skip frontend build (use existing dist)"
    )
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="Skip dependency checks"
    )
    
    args = parser.parse_args()
    
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 60)
    print("ChuQin PyWebView Build Script")
    print("=" * 60)
    print(f"{Colors.ENDC}")
    
    # Check dependencies
    if not args.skip_deps:
        if not check_dependencies():
            sys.exit(1)
    
    # Build frontend
    if not args.skip_frontend:
        if not build_frontend():
            sys.exit(1)
    
    # Build application
    if not build_app(target_platform=args.platform):
        sys.exit(1)
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}Build completed successfully!{Colors.ENDC}")


if __name__ == "__main__":
    main()
