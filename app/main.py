import os
import re
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


def get_gitconfig_path():
    """
    Get the path to the user's .gitconfig file.
    """
    home = Path.home()
    gitconfig_path = home / ".gitconfig"
    return str(gitconfig_path)


def read_gitconfig():
    """
    Read and parse the .gitconfig file.
    Returns a list of config entries with their structure.
    """
    gitconfig_path = get_gitconfig_path()
    
    if not os.path.exists(gitconfig_path):
        return {
            "success": True,
            "entries": [],
            "raw_content": ""
        }
    
    try:
        with open(gitconfig_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = []
        lines = content.split('\n')
        current_section = None
        current_subsection = None
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                entries.append({
                    "type": "empty",
                    "line_number": i + 1,
                    "raw": line
                })
                continue
            
            # Check if line is commented (disabled) - but preserve original for pure comments
            is_disabled = stripped.startswith('#')
            original_stripped = stripped
            
            # Pure comment line (starts with # and is not a disabled config)
            if is_disabled and not re.match(r'#\s*\[', stripped) and not re.match(r'#\s*\S+\s*=', stripped):
                entries.append({
                    "type": "comment",
                    "line_number": i + 1,
                    "raw": line
                })
                continue
            
            # Remove # prefix for disabled configs
            if is_disabled:
                stripped = stripped[1:].strip()
            
            # Section header: [section "subsection"] or [section]
            section_match = re.match(r'\[([^\]]+)\]', stripped)
            if section_match:
                section_str = section_match.group(1)
                parts = section_str.split('"', 1)
                if len(parts) == 2:
                    current_section = parts[0].strip()
                    current_subsection = parts[1].rstrip('"').strip()
                else:
                    current_section = section_str.strip()
                    current_subsection = None
                
                entries.append({
                    "type": "section",
                    "line_number": i + 1,
                    "section": current_section,
                    "subsection": current_subsection,
                    "disabled": is_disabled,
                    "raw": line
                })
                continue
            
            # Key-value pair: key = value
            kv_match = re.match(r'(\S+)\s*=\s*(.*)$', stripped)
            if kv_match:
                key = kv_match.group(1).strip()
                value = kv_match.group(2).strip()
                
                entries.append({
                    "type": "config",
                    "line_number": i + 1,
                    "section": current_section,
                    "subsection": current_subsection,
                    "key": key,
                    "value": value,
                    "disabled": is_disabled,
                    "raw": line
                })
                continue
            
            # Unknown line type - preserve as-is
            entries.append({
                "type": "unknown",
                "line_number": i + 1,
                "raw": line
            })
        
        return {
            "success": True,
            "entries": entries,
            "raw_content": content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "entries": [],
            "raw_content": ""
        }


def write_gitconfig(entries):
    """
    Write config entries back to .gitconfig file.
    entries: List of entry objects with structure from read_gitconfig
    """
    gitconfig_path = get_gitconfig_path()
    
    try:
        lines = []
        for entry in entries:
            if entry.get("type") == "empty":
                lines.append("")
            elif entry.get("type") == "section":
                section = entry.get("section", "")
                subsection = entry.get("subsection")
                disabled = entry.get("disabled", False)
                
                if subsection:
                    section_str = f'[{section} "{subsection}"]'
                else:
                    section_str = f'[{section}]'
                
                if disabled:
                    lines.append(f"# {section_str}")
                else:
                    lines.append(section_str)
            elif entry.get("type") == "config":
                key = entry.get("key", "")
                value = entry.get("value", "")
                disabled = entry.get("disabled", False)
                
                # Add space indentation before config key-value pairs (4 spaces)
                indent = "    "  # 4 spaces
                if disabled:
                    # For disabled configs, add spaces before the comment
                    config_line = f"{indent}# {key} = {value}"
                else:
                    config_line = f"{indent}{key} = {value}"
                lines.append(config_line)
            elif entry.get("type") == "comment":
                lines.append(entry.get("raw", ""))
            elif entry.get("type") == "unknown":
                lines.append(entry.get("raw", ""))
            else:
                # Fallback: use raw content
                lines.append(entry.get("raw", ""))
        
        content = '\n'.join(lines)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(gitconfig_path), exist_ok=True)
        
        with open(gitconfig_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


class Api:
    """API class to expose Python functions to JavaScript"""
    def read_gitconfig(self):
        return read_gitconfig()
    
    def write_gitconfig(self, entries):
        return write_gitconfig(entries)
    
    def get_gitconfig_path(self):
        return get_gitconfig_path()


def main():
    url = get_portal_url()

    # Expose Python functions to JavaScript using a class
    api = Api()

    window = webview.create_window(
        title='ChuQin',
        url=url,
        width=1200,
        height=800,
        min_size=(600, 500),
        resizable=True,
        js_api=api
    )

    webview.start(debug=False)


if __name__ == "__main__":
    main()
