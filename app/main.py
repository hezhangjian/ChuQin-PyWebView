import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import webview


def get_resource_path():
    """
    Get the base path for resources.
    In PyInstaller bundle, use sys._MEIPASS, otherwise use project root.
    """
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        return Path(sys._MEIPASS)
    else:
        # Running as script
        return Path(__file__).parent.parent


def get_portal_url():
    """
    Get the URL to load the frontend application.
    Returns the built dist folder if it exists, otherwise starts dev server.
    """
    # Get the base path (handles both bundled and development modes)
    base_path = get_resource_path()
    dist_dir = base_path / "portal" / "dist"
    index_html = dist_dir / "index.html"

    # Check if dist folder exists with index.html
    if dist_dir.exists() and index_html.exists():
        # Use built static files - pywebview accepts file paths directly
        return str(index_html.absolute())
    else:
        # Only start dev server in development mode (not in bundle)
        if getattr(sys, 'frozen', False):
            raise RuntimeError(
                "Frontend files not found in bundle. "
                "Please rebuild the application with 'python build.py'."
            )
        # Start Vite dev server (development mode only)
        project_root = Path(__file__).parent.parent
        portal_dir = project_root / "portal"
        return start_dev_server(portal_dir)


def start_dev_server(portal_dir):
    """
    Start Vite development server and return the URL.
    """
    # Check if node_modules exists
    node_modules = portal_dir / "node_modules"
    if not node_modules.exists():
        raise RuntimeError(
            "Frontend dependencies not installed. "
            "Please run 'pnpm install' in the portal directory."
        )

    # Start Vite dev server
    # Use pnpm if pnpm-lock.yaml exists, otherwise use npm
    lock_file = portal_dir / "pnpm-lock.yaml"
    if lock_file.exists():
        cmd = ["pnpm", "dev"]
    else:
        cmd = ["npm", "run", "dev"]

    # Start the dev server in background
    process = subprocess.Popen(
        cmd,
        cwd=str(portal_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for server to start (default Vite port is 5173)
    dev_url = "http://localhost:5173"
    max_wait = 10  # seconds
    waited = 0

    while waited < max_wait:
        try:
            urllib.request.urlopen(dev_url, timeout=1)
            break
        except Exception:
            time.sleep(0.5)
            waited += 0.5

    if waited >= max_wait:
        raise RuntimeError("Failed to start Vite dev server")

    return dev_url


def main():
    url = get_portal_url()

    window = webview.create_window(
        title='ChuQin',
        url=url,
        width=1200,
        height=800,
        min_size=(600, 500),
        resizable=True
    )

    webview.start(debug=False)


if __name__ == "__main__":
    main()
