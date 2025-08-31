import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from urllib.parse import urlparse, parse_qs
import webbrowser
import os
import sys

# Insert values for API credentials
SPOTIPY_CLIENT_ID = 'REDACTED'
SPOTIPY_CLIENT_SECRET = 'REDACTED'
SPOTIPY_REDIRECT_URI = 'REDACTED'  # must match your Spotify app
SCOPE = 'playlist-modify-public playlist-modify-private'

# Get absolute path to resource
def resource_path(relative_path):
    
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Song ID extractor from Spotify track URL
def extract_track_id(url: str):
    parts = url.split('/')
    if len(parts) > 4 and parts[3] == 'track':
        return parts[4].split('?')[0]
    return None
# Playlist name entering and validation
def get_playlist_name(root):
    while True:
        playlist_name = simpledialog.askstring("Playlist Name", "Enter your playlist name:")
        if playlist_name:
            return playlist_name
        else:
            messagebox.showwarning("Input Required", "Playlist Name is required.")
# Spotify user validation token input, extractor and validation
def get_redirect_url(root):
    while True:
        redirect_url = simpledialog.askstring(
            "Redirect URL",
            "Paste the full URL you were redirected to after login:"
        )
        if not redirect_url:
            messagebox.showerror("Error", "Redirect URL is required.")
            continue

        parsed_url = urlparse(redirect_url)
        code = parse_qs(parsed_url.query).get('code')
        if not code:
            messagebox.showwarning("Invalid URL", "URL provided is invalid. Please provide a valid URL.")
            continue

        return redirect_url, code[0]
# File path selection for user track URLs and validation
def get_user_file_path(root):
    messagebox.showinfo("File Selection", "Please select text file containing Spotify URL's (Limit 100)")
    file_path = filedialog.askopenfilename(
        title="Select file with Spotify track URLs",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not file_path or not os.path.isfile(file_path):
        messagebox.showerror("Error", "A valid file must be selected.")
        return None
    return file_path

def main():
    root = tk.Tk()
    root.withdraw()

    # Set window icon
    icon_path = resource_path('my_logo.ico')
    try:
        root.iconbitmap(icon_path)
    except tk.TclError:
        pass

    # Show authorization notice popup before opening URL
    messagebox.showinfo(
        "Authorization",
        "You will be requested to authorize Spotify to application. Please do not close the link."
    )
    # Spotify OAuth object
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True
    )
    # Open authorization URL in browser
    auth_url = sp_oauth.get_authorize_url()
    print("Please go to this URL to authorize:")
    print(auth_url)
    webbrowser.open(auth_url)
    # Get playlist name and description
    playlist_name = get_playlist_name(root)
    playlist_desc = simpledialog.askstring("Playlist Description", "Enter playlist description (optional):")
    if playlist_desc is None:
        playlist_desc = ""

    redirect_url, code = get_redirect_url(root)
    
    file_path = None
    while not file_path:
        file_path = get_user_file_path(root)
    # Get access token
    access_token = sp_oauth.get_access_token(code, as_dict=False)
    if not access_token:
        messagebox.showerror("Error", "Failed to get access token.")
        return
    # Create Spotify client
    sp = spotipy.Spotify(auth=access_token)
    user_id = sp.current_user()['id']

    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    # Extract track URIs from URLs
    track_uris = []
    for url in urls:
        track_id = extract_track_id(url)
        if track_id:
            track_uris.append(f"spotify:track:{track_id}")
    # Validate extracted track URIs
    if not track_uris:
        messagebox.showerror("Error", "No valid track URLs found in the file.")
        return
    # Create playlist
    print("Creating playlist...")
    playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=True,
        description=playlist_desc
    )
    playlist_id = playlist['id']
    # Add tracks to playlist
    print(f"Adding {len(track_uris)} tracks to playlist...")
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(playlist_id, track_uris[i:i + 100])

    print(f"Playlist '{playlist_name}' created successfully with {len(track_uris)} tracks!")

    # Show success popup
    success_root = tk.Tk()
    success_root.withdraw()
    try:
        success_root.iconbitmap(icon_path)
    except tk.TclError:
        pass
    messagebox.showinfo(
        "Success",
        f"Playlist '{playlist_name}' created successfully with {len(track_uris)} tracks!"
    )
    success_root.destroy()

if __name__ == "__main__":
    main()
