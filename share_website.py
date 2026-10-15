"""
GlowCare - Instant Public Sharing Launcher
Launches the Flask application and creates a public shareable HTTPS link.
"""
import os
import sys
import subprocess
import time
import urllib.request

def get_public_ip():
    """Fetch public IP for LocalTunnel password bypass if required."""
    try:
        with urllib.request.urlopen('https://api.ipify.org', timeout=5) as response:
            return response.read().decode('utf-8').strip()
    except Exception:
        return 'your public IP'

def main():
    print("=" * 65)
    print("  ✨ GLOWCARE - PUBLIC WEBSHARE LAUNCHER")
    print("=" * 65)
    print("\n[1/2] Starting Flask local server on port 5000...")
    
    # Start Flask app as subprocess
    flask_proc = subprocess.Popen([sys.executable, "app.py"])
    time.sleep(2)
    
    subdomain = "glowcare-app"
    ip = get_public_ip()
    
    print("\n[2/2] Generating public HTTPS link with project name...")
    print(f"\n✨ YOUR SHAREABLE PUBLIC LINK:")
    print(f"👉 https://{subdomain}.loca.lt")
    print(f"👉 Local URL: http://localhost:5000")
    print(f"\n💡 Note: If prompted for 'Tunnel Password' when opening the link:")
    print(f"   Enter this IP: {ip}")
    print("\n(Press Ctrl+C at any time to stop sharing)")
    print("=" * 65)
    
    # Launch localtunnel
    try:
        cmd = f'npx --yes localtunnel --port 5000 -s {subdomain}'
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        flask_proc.terminate()

if __name__ == "__main__":
    main()
