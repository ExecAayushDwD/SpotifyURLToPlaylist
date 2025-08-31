# URLs in text file to Spotify playlist 

## Overview

This API provides functionality to create Spotify playlists from text files containing Spotify track URLs. The application handles OAuth authentication, track URL parsing, and playlist creation through the Spotify Web API.

## Configuration

### Authentication Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `SPOTIPY_CLIENT_ID` | string | Spotify application client ID |
| `SPOTIPY_CLIENT_SECRET` | string | Spotify application client secret |
| `SPOTIPY_REDIRECT_URI` | string | Registered redirect URI for OAuth flow |
| `SCOPE` | string | Required permissions: `playlist-modify-public playlist-modify-private` |

## Core Functions

### `resource_path(relative_path: str) -> str`

Resolves resource file paths for both development and PyInstaller executable environments.

**Parameters:**

* `relative_path` (string): Path to resource file relative to application root

**Returns:**

* `string`: Absolute path to resource file

**Usage:**

```python
icon_path = resource_path('my_logo.ico')
```

### `extract_track_id(url: str) -> str | None`

Extracts Spotify track ID from a Spotify track URL.

**Parameters:**

* `url` (string): Spotify track URL in format `https://open.spotify.com/track/{track_id}`

**Returns:**

* `string`: Track ID if extraction successful
* `None`: If URL format is invalid

**Usage:**

```python
track_id = extract_track_id("https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh")
# Returns: "4iV5W9uYEdYUVa79Axb7Rh"
```

### `get_playlist_name(root: tk.Tk) -> str`

Prompts user for playlist name with validation loop.

**Parameters:**

* `root` (tk.Tk): Tkinter root window instance

**Returns:**

* `string`: User-provided playlist name

**Behavior:**

* Displays input dialog for playlist name
* Loops until valid name is provided
* Shows warning for empty input

### `get_redirect_url(root: tk.Tk) -> tuple[str, str]`

Handles OAuth redirect URL input and authorization code extraction.

**Parameters:**

* `root` (tk.Tk): Tkinter root window instance

**Returns:**

* `tuple`: (full\_redirect\_url, authorization\_code)

**Behavior:**

* Prompts user to paste OAuth redirect URL
* Validates URL contains authorization code
* Extracts code parameter from URL query string
* Loops until valid URL is provided

### `get_user_file_path(root: tk.Tk) -> str | None`

File selection dialog for track URL text files.

**Parameters:**

* `root` (tk.Tk): Tkinter root window instance

**Returns:**

* `string`: Selected file path
* `None`: If no valid file selected

**File Requirements:**

* Text files (.txt) preferred
* Maximum 100 track URLs
* One URL per line

## Main Workflow

### `main() -> None`

Orchestrates the complete playlist creation workflow.

**Process Flow:**

1. **UI Initialization**
    * Creates hidden Tkinter root window
    * Sets application icon
2. **OAuth Authentication**
    * Creates SpotifyOAuth instance
    * Opens authorization URL in browser
    * Handles user authorization flow
3. **User Input Collection**
    * Playlist name (required)
    * Playlist description (optional)
    * OAuth redirect URL
    * Track URLs file selection
4. **Token Exchange**
    * Exchanges authorization code for access token
    * Initializes Spotify client
5. **Track Processing**
    * Reads URLs from selected file
    * Extracts track IDs and creates Spotify URIs
    * Validates track data
6. **Playlist Creation**
    * Creates new public playlist
    * Adds tracks in batches of 100 (API limit)
    * Displays success confirmation

## API Endpoints Used

### Spotify Web API Integration

| Endpoint | Method | Purpose |
| -------- | ------ | ------- |
| `/me` | GET | Get current user profile |
| `/users/{user_id}/playlists` | POST | Create new playlist |
| `/playlists/{playlist_id}/tracks` | POST | Add tracks to playlist |

## Error Handling

### Authentication Errors

* Invalid credentials result in authorization failure
* Missing redirect URL shows error dialog
* Invalid OAuth code triggers re-authentication

### File Processing Errors

* Missing file selection shows error dialog
* Invalid file paths are rejected
* Empty or invalid track URLs are skipped

### API Errors

* Failed token exchange stops execution
* Invalid track URIs are filtered out
* Batch processing handles API limits

## Usage Example

```python
# Basic usage flow
if __name__ == "__main__":
    main()
```

**Required Setup:**

1. Configure Spotify app credentials
2. Prepare text file with Spotify track URLs
3. Run application and follow GUI prompts
4. Complete OAuth authorization in browser
5. Provide playlist details and file selection

**Output:**

* New Spotify playlist created in user's account
* Success confirmation with track count
* Console logging of process steps
