# osxphotos_mcp

<!-- markdownlint-disable MD013 MD004 MD007 MD029 MD030 MD032 -->

An MCP server for interacting with the `osxphotos` CLI tool.

This server provides a way for AI tools that support the Model Context Protocol (MCP) to interact with your Apple Photos library through the powerful `osxphotos` command-line tool.
 
## Quick Index

- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Testing](#testing)
- [Developer Documentation](#developer-documentation)
    - [Available Tools](#available-tools)
        - [about](#about)
        - [add_locations](#add_locations)
        - [albums](#albums)
        - [batch_edit](#batch_edit)
        - [compare](#compare)
        - [docs](#docs)
        - [dump](#dump)
        - [exiftool](#exiftool)
        - [export_photos](#export_photos)
        - [exportdb](#exportdb)
        - [help_command](#help_command)
        - [import_photos](#import_photos)
        - [info](#info)
        - [keywords](#keywords)
        - [labels](#labels)
        - [list_libraries](#list_libraries)
        - [orphans](#orphans)
        - [persons](#persons)
        - [places](#places)
        - [push_exif](#push_exif)
        - [query_photos](#query_photos)
        - [show](#show)
        - [sync](#sync)
        - [timewarp](#timewarp)
        - [tutorial](#tutorial)
        - [update](#update)
        - [uuid](#uuid)
        - [version](#version)
        - [install](#install)
        - [run](#run)
        - [uninstall](#uninstall)
- [Configure with common MCP clients](#configure-with-common-mcp-clients)
    - [Claude Desktop (macOS)](#claude-desktop-macos)
    - [VS Code – Continue extension](#vs-code--continue-extension)
    - [Zed editor](#zed-editor)
    - [gemini-cli (template)](#gemini-cli-template)

## Prerequisites

This server executes the `osxphotos` CLI. The executable is discovered in this order:

1. If the environment variable `OSXPHOTOS_BIN` is set to an absolute path to the executable, that path is used.
2. Otherwise, the system `PATH` is searched (same environment as the process that launches this server).

If the executable cannot be found, tools will return a clear error message asking you to set `OSXPHOTOS_BIN` or update `PATH`.

Tip: Verify discovery with the `osxphotos_health` tool. It reports the resolved path, `--version`, and relevant environment variables. If you’re running this from an app that manages its own environment, ensure the directory that contains `osxphotos` is on `PATH` (use `which osxphotos` to find it), or set `OSXPHOTOS_BIN` to the absolute path explicitly.

Python version: This server targets Python >= 3.12,<3.14. The setup instructions below create a Python 3.12 virtual environment. You can confirm the runtime with the `python_version` tool.

## Installation and Setup

1. **Clone the repository (or create the project files):**

    ```bash
    # (If you have the project files, you can skip this step)
    git clone <repository_url>
    cd osxphotos_mcp
    ```

2. **Create a virtual environment and install dependencies:**

    This project uses `uv` for package management. Make sure you have `uv` installed.

    ```bash
    # Create the virtual environment with Python 3.12 and install pip
    uv venv --python 3.12 --seed

    # Install the required packages
    .venv/bin/python -m pip install "mcp[cli]"
    ```

## Usage

To run the MCP server, execute the following command from the project's root directory:

```bash
uv run mcp dev main.py
```

This will start the server in development mode.

## Testing

Once the server is running, you can test it using the MCP Inspector, a web-based interface for interacting with the server's tools.

1. When you start the server, it will print a URL in your terminal, usually `http://localhost:6274`.
2. Open this URL in your web browser.
3. You will see all the available tools and their parameters.
4. You can expand each tool to see its parameters, fill them with test values, and click the "Execute" button to run the tool and see the output.

## Configure with common MCP clients

Below are examples for wiring this server into popular MCP clients. Use absolute paths to `main.py` and set `OSXPHOTOS_BIN` if your client is a GUI app (it may not inherit your shell PATH).

Tip: After adding a server, run `python_version` and `osxphotos_health` from your client to verify the environment.

### Claude Desktop (macOS)

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` and add an entry under `mcpServers`:

```json
{
    "mcpServers": {
        "osxphotos-mcp": {
            "command": "uv",
            "args": ["run", "mcp", "dev", "/absolute/path/to/main.py"],
            "env": {
                "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos"
            }
        }
    }
}
```

Then restart Claude Desktop.

### VS Code – Continue extension

Create or edit `~/.continue/config.json` (user-level) or `.continue/config.json` in your workspace:

```json
{
    "mcpServers": {
        "osxphotos-mcp": {
            "command": "uv",
            "args": ["run", "mcp", "dev", "/absolute/path/to/main.py"],
            "env": {
                "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos"
            }
        }
    }
}
```

Reload the Continue extension (or VS Code) and look for the server under Tools.

### Zed editor

Add a server entry to your Zed settings (e.g., `~/.config/zed/settings.json`). Insert under the root settings object:

```json
{
    "mcp": {
        "servers": [
            {
                "name": "osxphotos-mcp",
                "binary": "uv",
                "args": ["run", "mcp", "dev", "/absolute/path/to/main.py"],
                "env": { "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos" }
            }
        ]
    }
}
```

Restart Zed to pick up changes.

### gemini-cli (template)

If your `gemini-cli` supports MCP servers via a config file, the entry typically follows the same pattern as above. Use this as a template and consult the `gemini-cli` documentation for the exact config path and schema:

```json
{
    "mcpServers": {
        "osxphotos-mcp": {
            "command": "uv",
            "args": ["run", "mcp", "dev", "/absolute/path/to/main.py"],
            "env": { "OSXPHOTOS_BIN": "/absolute/path/to/osxphotos" }
        }
    }
}
```

Troubleshooting tips:

- GUI apps often have a minimal PATH. Prefer setting `OSXPHOTOS_BIN` to the absolute path of `osxphotos`.
- Ensure your Python matches the supported range (>= 3.12,< 3.14). Use the `python_version` tool to verify.
- Use `osxphotos_health` to confirm the resolved CLI path and version.

## Developer Documentation

### Available Tools

The server exposes tools for many of the commands available in the `osxphotos` CLI tool. Below is a detailed description of each tool and the parameters it exposes to AI tools.

#### `about`

Prints information about osxphotos including license.

Invokes the `osxphotos about` command.

**Parameters:** None

#### `add_locations`

Adds missing location data to photos in Photos.app using nearest neighbor.

Invokes the `osxphotos add-locations` command.

**Parameters:**

*   `window` (Optional[str]): Window of time to search for nearest neighbor.
*   `dry_run` (bool): Don't actually add location, just print what would be done.
*   `verbose` (bool): Print verbose output.
*   `timestamp` (bool): Add time stamp to verbose output.
*   `keyword` (Optional[List[str]]): Search for photos with keyword.
*   `no_keyword` (bool): Search for photos with no keyword.
*   `person` (Optional[List[str]]): Search for photos with person.
*   `album` (Optional[List[str]]): Search for photos in album.
*   `folder` (Optional[List[str]]): Search for photos in an album in folder.
*   `name` (Optional[List[str]]): Search for photos with filename matching.
*   `uuid` (Optional[List[str]]): Search for photos with UUID(s).
*   `uuid_from_file` (Optional[str]): Search for photos with UUID(s) loaded from FILE.
*   `title` (Optional[str]): Search for TITLE in title of photo.
*   `no_title` (bool): Search for photos with no title.
*   `description` (Optional[str]): Search for DESC in description of photo.
*   `no_description` (bool): Search for photos with no description.
*   `place` (Optional[str]): Search for PLACE in photo's reverse geolocation info.
*   `no_place` (bool): Search for photos with no associated place name info.
*   `location` (bool): Search for photos with associated location info.
*   `no_location` (bool): Search for photos with no associated location info.
*   `label` (Optional[List[str]]): Search for photos with image classification label.
*   `uti` (Optional[str]): Search for photos whose uniform type identifier (UTI) matches.
*   `ignore_case` (bool): Case insensitive search.
*   `edited` (bool): Search for photos that have been edited.
*   `not_edited` (bool): Search for photos that have not been edited.
*   `external_edit` (bool): Search for photos edited in external editor.
*   `favorite` (bool): Search for photos marked favorite.
*   `not_favorite` (bool): Search for photos not marked favorite.
*   `hidden` (bool): Search for photos marked hidden.
*   `not_hidden` (bool): Search for photos not marked hidden.
*   `shared` (bool): Search for photos in shared iCloud album.
*   `not_shared` (bool): Search for photos not in shared iCloud album.
*   `burst` (bool): Search for photos that were taken in a burst.
*   `not_burst` (bool): Search for photos that are not part of a burst.
*   `live` (bool): Search for Apple live photos.
*   `not_live` (bool): Search for photos that are not Apple live photos.
*   `portrait` (bool): Search for Apple portrait mode photos.
*   `not_portrait` (bool): Search for photos that are not Apple portrait mode photos.
*   `screenshot` (bool): Search for screenshot photos.
*   `not_screenshot` (bool): Search for photos that are not screenshot photos.
*   `screen_recording` (bool): Search for screen-recording videos.
*   `not_screen_recording` (bool): Search for photos that are not screen recording videos.
*   `slow_mo` (bool): Search for slow motion videos.
*   `not_slow_mo` (bool): Search for photos that are not slow motion videos.
*   `time_lapse` (bool): Search for time lapse videos.
*   `not_time_lapse` (bool): Search for photos that are not time lapse videos.
*   `hdr` (bool): Search for high dynamic range (HDR) photos.
*   `not_hdr` (bool): Search for photos that are not HDR photos.
*   `selfie` (bool): Search for selfies.
*   `not_selfie` (bool): Search for photos that are not selfies.
*   `panorama` (bool): Search for panorama photos.
*   `not_panorama` (bool): Search for photos that are not panoramas.
*   `has_raw` (bool): Search for photos with both a jpeg and raw version.
*   `only_movies` (bool): Search only for movies.
*   `only_photos` (bool): Search only for photos/images.
*   `from_date` (Optional[str]): Search for items created on or after DATE.
*   `to_date` (Optional[str]): Search for items created before DATE.
*   `from_time` (Optional[str]): Search for items created on or after TIME of day.
*   `to_time` (Optional[str]): Search for items created before TIME of day.
*   `year` (Optional[List[int]]): Search for items from a specific year.
*   `added_before` (Optional[str]): Search for items added to the library before a specific date/time.
*   `added_after` (Optional[str]): Search for items added to the library on or after a specific date/time.
*   `added_in_last` (Optional[str]): Search for items added to the library in the last TIME_DELTA.
*   `has_comment` (bool): Search for photos that have comments.
*   `no_comment` (bool): Search for photos with no comments.
*   `has_likes` (bool): Search for photos that have likes.
*   `no_likes` (bool): Search for photos with no likes.
*   `is_reference` (bool): Search for photos that were imported as referenced files.
*   `not_reference` (bool): Search for photos that are not references.
*   `in_album` (bool): Search for photos that are in one or more albums.
*   `not_in_album` (bool): Search for photos that are not in any albums.
*   `duplicate` (bool): Search for photos with possible duplicates.
*   `min_size` (Optional[str]): Search for photos with size >= SIZE bytes.
*   `max_size` (Optional[str]): Search for photos with size <= SIZE bytes.
*   `missing` (bool): Search for photos missing from disk.
*   `not_missing` (bool): Search for photos present on disk.
*   `cloudasset` (bool): Search for photos that are part of an iCloud library.
*   `not_cloudasset` (bool): Search for photos that are not part of an iCloud library.
*   `incloud` (bool): Search for photos that are in iCloud.
*   `not_incloud` (bool): Search for photos that are not in iCloud.
*   `syndicated` (bool): Search for photos that have been shared via syndication.
*   `not_syndicated` (bool): Search for photos that have not been shared via syndication.
*   `saved_to_library` (bool): Search for syndicated photos that have saved to the library.
*   `not_saved_to_library` (bool): Search for syndicated photos that have not saved to the library.
*   `shared_moment` (bool): Search for photos that are part of a shared moment.
*   `not_shared_moment` (bool): Search for photos that are not part of a shared moment.
*   `shared_library` (bool): Search for photos that are part of a shared library.
*   `not_shared_library` (bool): Search for photos that are not part of a shared library.
*   `regex` (Optional[List[str]]): Search for photos where TEMPLATE matches regular expression REGEX.
*   `selected` (bool): Filter for photos that are currently selected in Photos.
*   `exif` (Optional[List[str]]): Search for photos where EXIF_TAG exists in photo's EXIF data and contains VALUE.
*   `query_eval` (Optional[List[str]]): Evaluate CRITERIA to filter photos.
*   `query_function` (Optional[List[str]]): Run function to filter photos.
*   `theme` (Optional[Literal['dark', 'light', 'mono', 'plain']]): Specify the color theme to use for output.

#### `albums`

Prints out albums found in the Photos library.

Invokes the `osxphotos albums` command.

**Parameters:**
*   `library` (Optional[str]): Specify path to Photos library.
*   `json` (bool): Print output in JSON format.

#### `batch_edit`

Batch edits photo metadata such as title, description, keywords, etc. Operates on currently selected photos.

Invokes the `osxphotos batch-edit` command.

**Parameters:**
*   `title` (Optional[str]): Set title of photo.
*   `description` (Optional[str]): Set description of photo.
*   `keyword` (Optional[List[str]]): Add keywords to photo.
*   `replace_keywords` (bool): When specified with --keyword, replace existing keywords.
*   `location` (Optional[List[float]]): Set location of photo.
*   `album` (Optional[List[str]]): Add photo to album ALBUM_TEMPLATE.
*   `split_folder` (Optional[str]): Automatically create hierarchal folders for albums.
*   `dry_run` (bool): Don't actually change anything.
*   `undo` (bool): Restores photo metadata to what it was prior to the last batch edit.
*   `verbose` (bool): Print verbose output.
*   `timestamp` (bool): Add time stamp to verbose output.
*   `theme` (Optional[Literal['dark', 'light', 'mono', 'plain']]): Specify the color theme to use for output.
*   `library` (Optional[str]): Specify Photos library path.

#### `compare`

Compares two Photos libraries to find differences.

Invokes the `osxphotos compare` command.

**Parameters:**
*   `library_a` (str): First Photos library to compare.
*   `library_b` (str): Second Photos library to compare.
*   `check` (bool): Check if libraries are different and print out total number of differences.
*   `csv` (bool): Output results in CSV (comma delimited) format.
*   `tsv` (bool): Output results in TSV (tab delimited) format.
*   `json` (bool): Output results in JSON format.
*   `output` (Optional[str]): Output file.
*   `signature` (Optional[str]): Custom template for signature.
*   `verbose` (bool): Print verbose output.

#### `docs`

Opens osxphotos documentation in your browser.

Invokes the `osxphotos docs` command.

**Parameters:** None

#### `dump`

**DEPRECATED:** Prints list of all photos & associated info from the Photos library. Use `query` instead.

Invokes the `osxphotos dump` command.

**Parameters:**
*   `library` (Optional[str]): Specify path to Photos library.
*   `json` (bool): Print output in JSON format.
*   `deleted_only` (bool): Include only photos from the 'Recently Deleted' folder.
*   `deleted` (bool): Include photos from the 'Recently Deleted' folder.
*   `field` (Optional[List[str]]): Output only specified custom fields.
*   `print_template` (Optional[List[str]]): Render TEMPLATE string for each photo queried and print to stdout.

#### `exiftool`

Runs exiftool on previously exported files to update metadata.

Invokes the `osxphotos exiftool` command.

**Parameters:**
*   `export_directory` (str): Directory where photos were exported.
*   `db_config` (bool): Load configuration options from the export database.
*   `load_config` (Optional[str]): Load options from file.
*   `save_config` (Optional[str]): Save options to file.
*   `exiftool_path` (Optional[str]): Optionally specify path to exiftool.
*   `exiftool_option` (Optional[List[str]]): Optional flag/option to pass to exiftool.
*   `exiftool_merge_keywords` (bool): Merge any keywords found in the original file with keywords from Photos.
*   `exiftool_merge_persons` (bool): Merge any persons found in the original file with persons from Photos.
*   `ignore_date_modified` (bool): Ignore the photo modification date and set EXIF:ModifyDate to EXIF:DateTimeOriginal.
*   `person_keyword` (bool): Use person in image as keyword/tag when writing metadata.
*   `album_keyword` (bool): Use album name as keyword/tag when writing metadata.
*   `keyword_template` (Optional[List[str]]): Specify a template string to use as keyword.
*   `replace_keywords` (bool): Replace keywords with any values specified with --keyword-template.
*   `description_template` (Optional[str]): Specify a template string to use as description.
*   `exportdb` (Optional[str]): Optional path to export database.
*   `report` (Optional[str]): Write a report of all files that were processed.
*   `append` (bool): If used with --report, add data to existing report file.
*   `verbose` (bool): Print verbose output.
*   `timestamp` (bool): Add time stamp to verbose output.
*   `dry_run` (bool): Run in dry-run mode.
*   `theme` (Optional[Literal['dark', 'light', 'mono', 'plain']]): Specify the color theme to use for output.
*   `library` (Optional[str]): Specify path to Photos library.

#### `export_photos`

Exports photos from the Photos database.

Invokes the `osxphotos export` command.

**Parameters:**
*   `dest` (str): Export path.
*   `library` (Optional[str]): Specify path to Photos library.
*   `verbose` (bool): Print verbose output.
*   `timestamp` (bool): Add time stamp to verbose output.
*   `no_progress` (bool): Do not display progress bar during export.
*   `keyword` (Optional[List[str]]): Search for photos with keyword.
*   `no_keyword` (bool): Search for photos with no keyword.
*   `person` (Optional[List[str]]): Search for photos with person.
*   `album` (Optional[List[str]]): Search for photos in album.
*   `folder` (Optional[List[str]]): Search for photos in an album in folder.
*   `name` (Optional[List[str]]): Search for photos with filename matching.
*   `uuid` (Optional[List[str]]): Search for photos with UUID(s).
*   `uuid_from_file` (Optional[str]): Search for photos with UUID(s) loaded from FILE.
*   `title` (Optional[str]): Search for TITLE in title of photo.
*   `no_title` (bool): Search for photos with no title.
*   `description` (Optional[str]): Search for DESC in description of photo.
*   `no_description` (bool): Search for photos with no description.
*   `place` (Optional[str]): Search for PLACE in photo's reverse geolocation info.
*   `no_place` (bool): Search for photos with no associated place name info.
*   `location` (bool): Search for photos with associated location info.
*   `no_location` (bool): Search for photos with no associated location info.
*   `label` (Optional[List[str]]): Search for photos with image classification label.
*   `uti` (Optional[str]): Search for photos whose uniform type identifier (UTI) matches.
*   `ignore_case` (bool): Case insensitive search.
*   `edited` (bool): Search for photos that have been edited.
*   `not_edited` (bool): Search for photos that have not been edited.
*   `external_edit` (bool): Search for photos edited in external editor.
*   `favorite` (bool): Search for photos marked favorite.
*   `not_favorite` (bool): Search for photos not marked favorite.
*   `hidden` (bool): Search for photos marked hidden.
*   `not_hidden` (bool): Search for photos not marked hidden.
*   `shared` (bool): Search for photos in shared iCloud album.
*   `not_shared` (bool): Search for photos not in shared iCloud album.
*   `burst` (bool): Search for photos that were taken in a burst.
*   `not_burst` (bool): Search for photos that are not part of a burst.
*   `live` (bool): Search for Apple live photos.
*   `not_live` (bool): Search for photos that are not Apple live photos.
*   `portrait` (bool): Search for Apple portrait mode photos.
*   `not_portrait` (bool): Search for photos that are not Apple portrait mode photos.
*   `screenshot` (bool): Search for screenshot photos.
*   `not_screenshot` (bool): Search for photos that are not screenshot photos.
*   `screen_recording` (bool): Search for screen-recording videos.
*   `not_screen_recording` (bool): Search for photos that are not screen recording videos.
*   `slow_mo` (bool): Search for slow motion videos.
*   `not_slow_mo` (bool): Search for photos that are not slow motion videos.
*   `time_lapse` (bool): Search for time lapse videos.
*   `not_time_lapse` (bool): Search for photos that are not time lapse videos.
*   `hdr` (bool): Search for high dynamic range (HDR) photos.
*   `not_hdr` (bool): Search for photos that are not HDR photos.
*   `selfie` (bool): Search for selfies.
*   `not_selfie` (bool): Search for photos that are not selfies.
*   `panorama` (bool): Search for panorama photos.
*   `not_panorama` (bool): Search for photos that are not panoramas.
*   `has_raw` (bool): Search for photos with both a jpeg and raw version.
*   `only_movies` (bool): Search only for movies.
*   `only_photos` (bool): Search only for photos/images.
*   `from_date` (Optional[str]): Search for items created on or after DATE.
*   `to_date` (Optional[str]): Search for items created before DATE.
*   `from_time` (Optional[str]): Search for items created on or after TIME of day.
*   `to_time` (Optional[str]): Search for items created before TIME of day.
*   `year` (Optional[List[int]]): Search for items from a specific year.
*   `added_before` (Optional[str]): Search for items added to the library before a specific date/time.
*   `added_after` (Optional[str]): Search for items added to the library on or after a specific date/time.
*   `added_in_last` (Optional[str]): Search for items added to the library in the last TIME_DELTA.
*   `has_comment` (bool): Search for photos that have comments.
*   `no_comment` (bool): Search for photos with no comments.
*   `has_likes` (bool): Search for photos that have likes.
*   `no_likes` (bool): Search for photos with no likes.
*   `is_reference` (bool): Search for photos that were imported as referenced files.
*   `not_reference` (bool): Search for photos that are not references.
*   `in_album` (bool): Search for photos that are in one or more albums.
*   `not_in_album` (bool): Search for photos that are not in any albums.
*   `duplicate` (bool): Search for photos with possible duplicates.
*   `min_size` (Optional[str]): Search for photos with size >= SIZE bytes.
*   `max_size` (Optional[str]): Search for photos with size <= SIZE bytes.
*   `missing` (bool): Search for photos missing from disk.
*   `not_missing` (bool): Search for photos present on disk.
*   `cloudasset` (bool): Search for photos that are part of an iCloud library.
*   `not_cloudasset` (bool): Search for photos that are not part of an iCloud library.
*   `incloud` (bool): Search for photos that are in iCloud.
*   `not_incloud` (bool): Search for photos that are not in iCloud.
*   `syndicated` (bool): Search for photos that have been shared via syndication.
*   `not_syndicated` (bool): Search for photos that have not been shared via syndication.
*   `saved_to_library` (bool): Search for syndicated photos that have saved to the library.
*   `not_saved_to_library` (bool): Search for syndicated photos that have not saved to the library.
*   `shared_moment` (bool): Search for photos that are part of a shared moment.
*   `not_shared_moment` (bool): Search for photos that are not part of a shared moment.
*   `shared_library` (bool): Search for photos that are part of a shared library.
*   `not_shared_library` (bool): Search for photos that are not part of a shared library.
*   `regex` (Optional[List[str]]): Search for photos where TEMPLATE matches regular expression REGEX.
*   `selected` (bool): Filter for photos that are currently selected in Photos.
*   `exif` (Optional[List[str]]): Search for photos where EXIF_TAG exists in photo's EXIF data and contains VALUE.
*   `query_eval` (Optional[List[str]]): Evaluate CRITERIA to filter photos.
*   `query_function` (Optional[List[str]]): Run function to filter photos.
*   `deleted_only` (bool): Include only photos from the 'Recently Deleted' folder.
*   `deleted` (bool): Include photos from the 'Recently Deleted' folder.
*   `update` (bool): Only export new or updated files.
*   `force_update` (bool): Only export new or updated files, re-exporting if metadata changed.
*   `update_errors` (bool): Update files that were previously exported but produced errors.
*   `ignore_signature` (bool): When used with '--update', ignores file signature when updating files.
*   `only_new` (bool): If used with --update, ignores any previously exported files, even if missing.
*   `limit` (Optional[int]): Export at most LIMIT photos.
*   `dry_run` (bool): Dry run (test) the export but don't actually export any files.
*   `export_as_hardlink` (bool): Hardlink files instead of copying them.
*   `touch_file` (bool): Sets the file's modification time to match photo date.
*   `overwrite` (bool): Overwrite existing files.
*   `retry` (Optional[int]): Automatically retry export up to RETRY times if an error occurs.
*   `export_by_date` (bool): Automatically create output folders to organize photos by date created.
*   `skip_edited` (bool): Do not export edited version of photo if an edited version exists.
*   `skip_original_if_edited` (bool): Do not export original if there is an edited version.
*   `skip_bursts` (bool): Do not export all associated burst images.
*   `skip_live` (bool): Do not export the associated live video component of a live photo.
*   `skip_raw` (bool): Do not export associated RAW image of a RAW+JPEG pair.
*   `skip_uuid` (Optional[List[str]]): Skip photos with UUID(s) during export.
*   `skip_uuid_from_file` (Optional[str]): Skip photos with UUID(s) loaded from FILE.
*   `current_name` (bool): Use photo's current filename instead of original filename for export.
*   `convert_to_jpeg` (bool): Convert all non-JPEG images to JPEG upon export.
*   `jpeg_quality` (Optional[float]): Value in range 0.0 to 1.0 to use with --convert-to-jpeg.
*   `fix_orientation` (bool): Automatically fix image orientation in exported photos.
*   `preview` (bool): Export preview image generated by Photos.
*   `preview_if_missing` (bool): Export preview image if the actual photo file is missing.
*   `preview_suffix` (Optional[str]): Optional suffix template for naming preview photos.
*   `download_missing` (bool): Attempt to download missing photos from iCloud.
*   `export_aae` (bool): Also export an adjustments file detailing edits made to the original.
*   `sidecar` (Optional[Literal['xmp', 'json', 'exiftool']]): Create sidecar for each photo exported.
*   `sidecar_drop_ext` (bool): Drop the photo's extension when naming sidecar files.
*   `sidecar_template` (Optional[List[str]]): Create a custom sidecar file for each photo exported with user provided Mako template.
*   `exiftool_flag` (bool): Use exiftool to write metadata directly to exported photos.
*   `exiftool_path` (Optional[str]): Optionally specify path to exiftool.
*   `exiftool_option` (Optional[List[str]]): Optional flag/option to pass to exiftool.
*   `exiftool_merge_keywords` (bool): Merge any keywords found in the original file with keywords used for '--exiftool' and '--sidecar'.
*   `exiftool_merge_persons` (bool): Merge any persons found in the original file with persons used for '--exiftool' and '--sidecar'.
*   `favorite_rating` (bool): When used with --exiftool or --sidecar, set XMP:Rating=5 for photos marked as Favorite.
*   `ignore_date_modified` (bool): If used with --exiftool or --sidecar, will ignore the photo modification date.
*   `person_keyword` (bool): Use person in image as keyword/tag when exporting metadata.
*   `album_keyword` (bool): Use album name as keyword/tag when exporting metadata.
*   `keyword_template` (Optional[List[str]]): Specify a template string to use as keyword.
*   `replace_keywords` (bool): Replace keywords with any values specified with --keyword-template.
*   `description_template` (Optional[str]): Specify a template string to use as description.
*   `finder_tag_template` (Optional[List[str]]): Set MacOS Finder tags to TEMPLATE.
*   `finder_tag_keywords` (bool): Set MacOS Finder tags to keywords.
*   `xattr_template` (Optional[List[str]]): Set extended attribute ATTRIBUTE to TEMPLATE value.
*   `directory` (Optional[str]): Optional template for specifying name of output directory.
*   `filename` (Optional[str]): Optional template for specifying name of output file.
*   `jpeg_ext` (Optional[str]): Specify file extension for JPEG files.
*   `strip` (bool): Optionally strip leading and trailing whitespace from any rendered templates.
*   `edited_suffix` (Optional[str]): Optional suffix template for naming edited photos.
*   `original_suffix` (Optional[str]): Optional suffix template for naming original photos.
*   `use_photos_export` (bool): Force the use of AppleScript or PhotoKit to export even if not missing.
*   `use_photokit` (bool): Use with '--download-missing' or '--use-photos-export' to use direct Photos interface.
*   `report` (Optional[str]): Write a report of all files that were exported.
*   `append` (bool): If used with --report, add data to existing report file.
*   `cleanup` (bool): Cleanup export directory by deleting any files which were not included in this export set.
*   `keep` (Optional[List[str]]): When used with --cleanup, prevents file or directory matching KEEP_RULE from being deleted.
*   `add_exported_to_album` (Optional[str]): Add all exported photos to album ALBUM in Photos.
*   `add_skipped_to_album` (Optional[str]): Add all skipped photos to album ALBUM in Photos.
*   `add_missing_to_album` (Optional[str]): Add all missing photos to album ALBUM in Photos.
*   `post_command` (Optional[List[str]]): Run COMMAND on exported files of category CATEGORY.
*   `post_command_error` (Optional[Literal['continue', 'break']]): Specify either 'continue' or 'break' for ACTION to control behavior when a post-command fails.
*   `post_function` (Optional[List[str]]): Run function on exported files.
*   `exportdb` (Optional[str]): Specify alternate path for database file which stores state information for export and --update.
*   `ramdb` (bool): Copy export database to memory during export.
*   `checkpoint` (Optional[int]): When used with --ramdb, periodically save the export database back to disk.
*   `ignore_exportdb` (bool): If exporting to a directory that already contains an export database and --update is not specified, do not prompt to continue.
*   `no_exportdb` (bool): Do not create an export database.
*   `tmpdir` (Optional[str]): Specify alternate temporary directory.
*   `alt_copy` (bool): Use alternate copy method that may be more reliable for some network attached storage (NAS) devices.
*   `alt_db` (Optional[str]): Specify alternate path to Photos library database.
*   `load_config` (Optional[str]): Load options from file as written with --save-config.
*   `save_config` (Optional[str]): Save options to file for use with --load-config.
*   `config_only` (bool): If specified, saves the config file but does not export any files.
*   `print_template` (Optional[List[str]]): Render TEMPLATE string for each photo being exported and print to stdout.
*   `theme` (Optional[Literal['dark', 'light', 'mono', 'plain']]): Specify the color theme to use for output.

#### `exportdb`

Utilities for working with the osxphotos export database.

Invokes the `osxphotos exportdb` command.

**Parameters:**
*   `export_database` (str): Path to the export database.
*   `version` (bool): Print export database version.
*   `vacuum` (bool): Run VACUUM to defragment the database.
*   `create` (Optional[str]): Create a new export database with VERSION.
*   `check_signatures` (bool): Check signatures for all exported photos in the database.
*   `update_signatures` (bool): Update signatures for all exported photos in the database.
*   `touch_file` (bool): Touch files on disk to match created date in Photos library.
*   `runs` (bool): List osxphotos commands used with this database.
*   `last_run` (bool): Show last run osxphotos commands used with this database.
*   `last_export_dir` (bool): Print path to last used export directory.
*   `save_config` (Optional[str]): Save last run configuration to TOML file.
*   `info` (Optional[str]): Print information about FILE_PATH contained in the database.
*   `errors` (bool): Print list of files that had warnings/errors on export.
*   `last_errors` (bool): Print list of files that had warnings/errors on last export run.
*   `uuid_files` (Optional[str]): List exported files associated with UUID.
*   `uuid_info` (Optional[str]): Print information about UUID contained in the database.
*   `history` (Optional[str]): Print history of FILE_PATH_OR_UUID contained in the database.
*   `delete_uuid` (Optional[str]): Delete all data associated with UUID from the database.
*   `delete_file` (Optional[str]): Delete all data associated with FILE_PATH from the database.
*   `report` (Optional[List[str]]): Generate an export report.
*   `upgrade` (bool): Upgrade (if needed) export database to current version.
*   `check` (bool): Check export database for errors.
*   `repair` (bool): Repair export database.
*   `sql` (Optional[str]): Execute SQL_STATEMENT against export database.
*   `migrate_photos_library` (Optional[str]): Migrate the export database to use the specified Photos library.
*   `export_dir` (Optional[str]): Optional path to export directory.
*   `append` (bool): If used with --report, add data to existing report file.
*   `verbose` (bool): Print verbose output.
*   `timestamp` (bool): Add time stamp to verbose output.
*   `theme` (Optional[Literal['dark', 'light', 'mono', 'plain']]): Specify the color theme to use for output.
*   `dry_run` (bool): Run in dry-run mode.

#### `help_command`

Prints help for osxphotos commands.

Invokes the `osxphotos help` command.

**Parameters:**
*   `command` (Optional[str]): The command to get help for.

#### `import_photos`

Imports photos and videos into Photos.

Invokes the `osxphotos import` command.

**Parameters:**
*   `files_or_dirs` (List[str]): Files or directories to import.
*   `album` (Optional[List[str]]): Import photos into album ALBUM_TEMPLATE.
*   `title` (Optional[str]): Set title of imported photos.
*   `description` (Optional[str]): Set description of imported photos.
*   `keyword` (Optional[List[str]]): Set keywords of imported photos.
*   `merge_keywords` (bool): Merge keywords with any keywords already associated with the photo.
*   `location` (Optional[List[float]]): Set location of imported photo.
*   `favorite_rating` (Optional[int]): If XMP:Rating is set to RATING or higher, mark imported photo as a favorite.
*   `auto_live` (bool): Automatically convert photo+video pairs into live images.
*   `parse_date` (Optional[str]): Parse date from filename using DATE_PATTERN.
*   `parse_folder_date` (Optional[str]): Parse date from folder name using DATE_PATTERN.
*   `clear_metadata` (bool): Clear any metadata set automatically by Photos upon import.
*   `clear_location` (bool): Clear any location data automatically imported by Photos.
*   `timezone` (Optional[str]): Set timezone for imported photos.
*   `exiftool` (bool): Use third party tool exiftool to automatically update metadata.
*   `exiftool_path` (Optional[str]): Optionally specify path to exiftool.
*   `sidecar` (bool): Use sidecar files to import metadata.
*   `sidecar_filename` (Optional[str]): Use sidecar files to import metadata.
*   `edited_suffix` (Optional[str]): Optional suffix template used for naming edited photos.
*   `sidecar_ignore_date` (bool): Do not use date/time in sidecar to set photo date/time.
*   `set_timezone` (bool): Set the named timezone of the imported photos in the Photos database.
*   `exportdb` (Optional[str]): Use an osxphotos export database to set metadata.
*   `exportdir` (Optional[str]): Specify the path to the export directory.
*   `relative_to` (Optional[str]): If set, the '{filepath}' template will be computed relative to RELATIVE_TO_PATH.
*   `dup_check` (bool): Use Photos' built-in duplicate checking.
*   `skip_dups` (bool): Skip duplicate photos on import.
*   `signature` (Optional[str]): Custom template for signature when using --skip-dups, --dup-check, and --dup-albums.
*   `dup_albums` (bool): If used with --skip-dups, the matching duplicate already in the Photos library will be added to any albums.
*   `split_folder` (Optional[str]): Automatically create hierarchal folders for albums.
*   `walk` (bool): Recursively walk through directories.
*   `glob` (Optional[List[str]]): Only import files matching GLOB.
*   `check` (bool): Check which FILES have been previously imported.
*   `check_not` (bool): Check which FILES have not been previously imported.
*   `dry_run` (bool): Dry run; do not actually import.
*   `report` (Optional[str]): Write a report of all files that were imported.
*   `resume` (bool): Resume previous import.
*   `append` (bool): If used with --report, add data to existing report file.
*   `verbose` (bool): Print verbose output.
*   `timestamp` (bool): Add time stamp to verbose output.
*   `no_progress` (bool): Do not display progress bar during import.
*   `check_templates` (bool): Don't actually import anything; renders template strings and date patterns.
*   `post_function` (Optional[List[str]]): Run python function after importing file.
*   `stop_on_error` (Optional[int]): Stops importing after COUNT errors.
*   `force` (bool): Bypass confirmation prompt.
*   `library` (Optional[str]): Path to the Photos library you are importing into.
*   `theme` (Optional[Literal['dark', 'light', 'mono', 'plain']]): Specify the color theme to use for output.

#### `info`

Prints out descriptive info of the Photos library database.

Invokes the `osxphotos info` command.

**Parameters:**
*   `library` (Optional[str]): Specify path to Photos library.
*   `json` (bool): Print output in JSON format.
*   `verbose` (bool): Print verbose output.

#### `keywords`

Prints out keywords found in the Photos library.

Invokes the `osxphotos keywords` command.

**Parameters:**
*   `library` (Optional[str]): Specify path to Photos library.
*   `json` (bool): Print output in JSON format.

#### `labels`

Prints out image classification labels found in the Photos library.

Invokes the `osxphotos labels` command.

**Parameters:**
*   `library` (Optional[str]): Specify path to Photos library.
*   `json` (bool): Print output in JSON format.

#### `list_libraries`

Prints list of Photos libraries found on the system.

Invokes the `osxphotos list` command.

**Parameters:**
*   `json` (bool): Print output in JSON format.

#### `orphans`

Finds orphaned photos in a Photos library.

Invokes the `osxphotos orphans` command.

**Parameters:**
*   `export` (Optional[str]): Export orphans to directory EXPORT_PATH.
*   `library` (Optional[str]): Specify path to Photos library.
*   `verbose` (bool): Print verbose output.
*   `timestamp` (bool): Add time stamp to verbose output.
*   `theme` (Optional[Literal['dark', 'light', 'mono', 'plain']]): Specify the color theme to use for output.

#### `persons`

Prints out persons (faces) found in the Photos library.

Invokes the `osxphotos persons` command.

**Parameters:**
*   `library` (Optional[str]): Specify path to Photos library.
*   `json` (bool): Print output in JSON format.

#### `places`

Prints out places found in the Photos library.

Invokes the `osxphotos places` command.

**Parameters:**
*   `library` (Optional[str]): Specify path to Photos library.
*   `json` (bool): Print output in JSON format.

#### `push_exif`

Writes photo metadata to original files in the Photos library.

Invokes the `osxphotos push-exif` command.

**Parameters:**
*   `metadata` (str): Metadata to push (e.g., 'all', 'keywords', 'location').
*   `push_edited` (bool): Push EXIF data to edited photos in addition to originals.
*   `exiftool_path` (Optional[str]): Optionally specify path to exiftool.
*   `exiftool_option` (Optional[List[str]]): Optional flag/option to pass to exiftool.
*   `exiftool_merge_keywords` (bool): Merge any keywords found in the original file with keywords from Photos.
*   `exiftool_merge_persons` (bool): Merge any persons found in the original file with persons from Photos.
*   `favorite_rating` (bool): Set XMP:Rating=5 for photos marked as Favorite.
*   `ignore_date_modified` (bool): Ignore the photo modification date.
*   `person_keyword` (bool): Use person in image as keyword/tag when writing metadata.
*   `album_keyword` (bool): Use album name as keyword/tag when writing metadata.
*   `keyword_template` (Optional[List[str]]): Specify a template string to use as keyword.
*   `replace_keywords` (bool): Replace keywords with any values specified with --keyword-template.
*   `description_template` (Optional[str]): Specify a template string to use as description.
*   `report` (Optional[str]): Write a report of all files that were processed.
*   `append` (bool): If used with --report, add data to existing report file.
*   `compare` (bool): Compare metadata only; do not push (write) metadata.
*   `dry_run` (bool): Dry run mode; show what would be done but do not actually write to any files.
*   `verbose` (bool): Print verbose output.
*   `timestamp` (bool): Add time stamp to verbose output.
*   `theme` (Optional[Literal['dark', 'light', 'mono', 'plain']]): Specify the color theme to use for output.
*   `library` (Optional[str]): Specify path to Photos library.
*   `keyword` (Optional[List[str]]): Search for photos with keyword.
*   `no_keyword` (bool): Search for photos with no keyword.
*   `person` (Optional[List[str]]): Search for photos with person.
*   `album` (Optional[List[str]]): Search for photos in album.
*   `folder` (Optional[List[str]]): Search for photos in an album in folder.
*   `name` (Optional[List[str]]): Search for photos with filename matching.
*   `uuid` (Optional[List[str]]): Search for photos with UUID(s).
*   `uuid_from_file` (Optional[str]): Search for photos with UUID(s) loaded from FILE.
*   `title` (Optional[str]): Search for TITLE in title of photo.
*   `no_title` (bool): Search for photos with no title.
*   `description` (Optional[str]): Search for DESC in description of photo.
*   `no_description` (bool): Search for photos with no description.
*   `place` (Optional[str]): Search for PLACE in photo's reverse geolocation info.
*   `no_place` (bool): Search for photos with no associated place name info.
*   `location` (bool): Search for photos with associated location info.
*   `no_location` (bool): Search for photos with no associated location info.
*   `label` (Optional[List[str]]): Search for photos with image classification label.
*   `uti` (Optional[str]): Search for photos whose uniform type identifier (UTI) matches.
*   `ignore_case` (bool): Case insensitive search.
*   `edited` (bool): Search for photos that have been edited.
*   `not_edited` (bool): Search for photos that have not been edited.
*   `external_edit` (bool): Search for photos edited in external editor.
*   `favorite` (bool): Search for photos marked favorite.
*   `not_favorite` (bool): Search for photos not marked favorite.
*   `hidden` (bool): Search for photos marked hidden.
*   `not_hidden` (bool): Search for photos not marked hidden.
*   `shared` (bool): Search for photos in shared iCloud album.
*   `not_shared` (bool): Search for photos not in shared iCloud album.
*   `burst` (bool): Search for photos that were taken in a burst.
*   `not_burst` (bool): Search for photos that are not part of a burst.
*   `live` (bool): Search for Apple live photos.
*   `not_live` (bool): Search for photos that are not Apple live photos.
*   `portrait` (bool): Search for Apple portrait mode photos.
*   `not_portrait` (bool): Search for photos that are not Apple portrait mode photos.
*   `screenshot` (bool): Search for screenshot photos.
*   `not_screenshot` (bool): Search for photos that are not screenshot photos.
*   `screen_recording` (bool): Search for screen-recording videos.
*   `not_screen_recording` (bool): Search for photos that are not screen recording videos.
*   `slow_mo` (bool): Search for slow motion videos.
*   `not_slow_mo` (bool): Search for photos that are not slow motion videos.
*   `time_lapse` (bool): Search for time lapse videos.
*   `not_time_lapse` (bool): Search for photos that are not time lapse videos.
*   `hdr` (bool): Search for high dynamic range (HDR) photos.
*   `not_hdr` (bool): Search for photos that are not HDR photos.
*   `selfie` (bool): Search for selfies.
*   `not_selfie` (bool): Search for photos that are not selfies.
*   `panorama` (bool): Search for panorama photos.
*   `not_panorama` (bool): Search for photos that are not panoramas.
*   `has_raw` (bool): Search for photos with both a jpeg and raw version.
*   `only_movies` (bool): Search only for movies.
*   `only_photos` (bool): Search only for photos/images.
*   `from_date` (Optional[str]): Search for items created on or after DATE.
*   `to_date` (Optional[str]): Search for items created before DATE.
*   `from_time` (Optional[str]): Search for items created on or after TIME of day.
*   `to_time` (Optional[str]): Search for items created before TIME of day.
*   `year` (Optional[List[int]]): Search for items from a specific year.
*   `added_before` (Optional[str]): Search for items added to the library before a specific date/time.
*   `added_after` (Optional[str]): Search for items added to the library on or after a specific date/time.
*   `added_in_last` (Optional[str]): Search for items added to the library in the last TIME_DELTA.
*   `has_comment` (bool): Search for photos that have comments.
*   `no_comment` (bool): Search for photos with no comments.
*   `has_likes` (bool): Search for photos that have likes.
*   `no_likes` (bool): Search for photos with no likes.
*   `is_reference` (bool): Search for photos that were imported as referenced files.
*   `not_reference` (bool): Search for photos that are not references.
*   `in_album` (bool): Search for photos that are in one or more albums.
*   `not_in_album` (bool): Search for photos that are not in any albums.
*   `duplicate` (bool): Search for photos with possible duplicates.
*   `min_size` (Optional[str]): Search for photos with size >= SIZE bytes.
*   `max_size` (Optional[str]): Search for photos with size <= SIZE bytes.
*   `missing` (bool): Search for photos missing from disk.
*   `not_missing` (bool): Search for photos present on disk.
*   `cloudasset` (bool): Search for photos that are part of an iCloud library.
*   `not_cloudasset` (bool): Search for photos that are not part of an iCloud library.
*   `incloud` (bool): Search for photos that are in iCloud.
*   `not_incloud` (bool): Search for photos that are not in iCloud.
*   `syndicated` (bool): Search for photos that have been shared via syndication.
*   `not_syndicated` (bool): Search for photos that have not been shared via syndication.
*   `saved_to_library` (bool): Search for syndicated photos that have saved to the library.
*   `not_saved_to_library` (bool): Search for syndicated photos that have not saved to the library.
*   `shared_moment` (bool): Search for photos that are part of a shared moment.
*   `not_shared_moment` (bool): Search for photos that are not part of a shared moment.
*   `shared_library` (bool): Search for photos that are part of a shared library.
*   `not_shared_library` (bool): Search for photos that are not part of a shared library.
*   `regex` (Optional[List[str]]): Search for photos where TEMPLATE matches regular expression REGEX.
*   `selected` (bool): Filter for photos that are currently selected in Photos.
*   `exif` (Optional[List[str]]): Search for photos where EXIF_TAG exists in photo's EXIF data and contains VALUE.
*   `query_eval` (Optional[List[str]]): Evaluate CRITERIA to filter photos.
*   `query_function` (Optional[List[str]]): Run function to filter photos.

#### `query_photos`

Queries the Photos database using 1 or more search options.

Invokes the `osxphotos query` command.

**Parameters:**
*   `library` (Optional[str]): Specify path to Photos library.
*   `json` (bool): Print output in JSON format.
*   `count` (bool): Print count of photos matching query and exit.
*   `keyword` (Optional[List[str]]): Search for photos with keyword.
*   `no_keyword` (bool): Search for photos with no keyword.
*   `person` (Optional[List[str]]): Search for photos with person.
*   `album` (Optional[List[str]]): Search for photos in album.
*   `folder` (Optional[List[str]]): Search for photos in an album in folder.
*   `name` (Optional[List[str]]): Search for photos with filename matching.
*   `uuid` (Optional[List[str]]): Search for photos with UUID(s).
*   `uuid_from_file` (Optional[str]): Search for photos with UUID(s) loaded from FILE.
*   `title` (Optional[str]): Search for TITLE in title of photo.
*   `no_title` (bool): Search for photos with no title.
*   `description` (Optional[str]): Search for DESC in description of photo.
*   `no_description` (bool): Search for photos with no description.
*   `place` (Optional[str]): Search for PLACE in photo's reverse geolocation info.
*   `no_place` (bool): Search for photos with no associated place name info.
*   `location` (bool): Search for photos with associated location info.
*   `no_location` (bool): Search for photos with no associated location info.
*   `label` (Optional[List[str]]): Search for photos with image classification label.
*   `uti` (Optional[str]): Search for photos whose uniform type identifier (UTI) matches.
*   `ignore_case` (bool): Case insensitive search.
*   `edited` (bool): Search for photos that have been edited.
*   `not_edited` (bool): Search for photos that have not been edited.
*   `external_edit` (bool): Search for photos edited in external editor.
*   `favorite` (bool): Search for photos marked favorite.
*   `not_favorite` (bool): Search for photos not marked favorite.
*   `hidden` (bool): Search for photos marked hidden.
*   `not_hidden` (bool): Search for photos not marked hidden.
*   `shared` (bool): Search for photos in shared iCloud album.
*   `not_shared` (bool): Search for photos not in shared iCloud album.
*   `burst` (bool): Search for photos that were taken in a burst.
*   `not_burst` (bool): Search for photos that are not part of a burst.
*   `live` (bool): Search for Apple live photos.
*   `not_live` (bool): Search for photos that are not Apple live photos.
*   `portrait` (bool): Search for Apple portrait mode photos.
*   `not_portrait` (bool): Search for photos that are not Apple portrait mode photos.
*   `screenshot` (bool): Search for screenshot photos.
*   `not_screenshot` (bool): Search for photos that are not screenshot photos.
*   `screen_recording` (bool): Search for screen-recording videos.
*   `not_screen_recording` (bool): Search for photos that are not screen recording videos.
*   `slow_mo` (bool): Search for slow motion videos.
*   `not_slow_mo` (bool): Search for photos that are not slow motion videos.
*   `time_lapse` (bool): Search for time lapse videos.
*   `not_time_lapse` (bool): Search for photos that are not time lapse videos.
*   `hdr` (bool): Search for high dynamic range (HDR) photos.
*   `not_hdr` (bool): Search for photos that are not HDR photos.
*   `selfie` (bool): Search for selfies.
*   `not_selfie` (bool): Search for photos that are not selfies.
*   `panorama` (bool): Search for panorama photos.
*   `not_panorama` (bool): Search for photos that are not panoramas.
*   `has_raw` (bool): Search for photos with both a jpeg and raw version.
*   `only_movies` (bool): Search only for movies.
*   `only_photos` (bool): Search only for photos/images.
*   `from_date` (Optional[str]): Search for items created on or after DATE.
*   `to_date` (Optional[str]): Search for items created before DATE.
*   `from_time` (Optional[str]): Search for items created on or after TIME of day.
*   `to_time` (Optional[str]): Search for items created before TIME of day.
*   `year` (Optional[List[int]]): Search for items from a specific year.
*   `added_before` (Optional[str]): Search for items added to the library before a specific date/time.
*   `added_after` (Optional[str]): Search for items added to the library on or after a specific date/time.
*   `added_in_last` (Optional[str]): Search for items added to the library in the last TIME_DELTA.
*   `has_comment` (bool): Search for photos that have comments.
*   `no_comment` (bool): Search for photos with no comments.
*   `has_likes` (bool): Search for photos that have likes.
*   `no_likes` (bool): Search for photos with no likes.
*   `is_reference` (bool): Search for photos that were imported as referenced files.
*   `not_reference` (bool): Search for photos that are not references.
*   `in_album` (bool): Search for photos that are in one or more albums.
*   `not_in_album` (bool): Search for photos that are not in any albums.
*   `duplicate` (bool): Search for photos with possible duplicates.
*   `min_size` (Optional[str]): Search for photos with size >= SIZE bytes.
*   `max_size` (Optional[str]): Search for photos with size <= SIZE bytes.
*   `missing` (bool): Search for photos missing from disk.
*   `not_missing` (bool): Search for photos present on disk.
*   `cloudasset` (bool): Search for photos that are part of an iCloud library.
*   `not_cloudasset` (bool): Search for photos that are not part of an iCloud library.
*   `incloud` (bool): Search for photos that are in iCloud.
*   `not_incloud` (bool): Search for photos that are not in iCloud.
*   `syndicated` (bool): Search for photos that have been shared via syndication.
*   `not_syndicated` (bool): Search for photos that have not been shared via syndication.
*   `saved_to_library` (bool): Search for syndicated photos that have saved to the library.
*   `not_saved_to_library` (bool): Search for syndicated photos that have not saved to the library.
*   `shared_moment` (bool): Search for photos that are part of a shared moment.
*   `not_shared_moment` (bool): Search for photos that are not part of a shared moment.
*   `shared_library` (bool): Search for photos that are part of a shared library.
*   `not_shared_library` (bool): Search for photos that are not part of a shared library.
*   `regex` (Optional[List[str]]): Search for photos where TEMPLATE matches regular expression REGEX.
*   `selected` (bool): Filter for photos that are currently selected in Photos.
*   `exif` (Optional[List[str]]): Search for photos where EXIF_TAG exists in photo's EXIF data and contains VALUE.
*   `query_eval` (Optional[List[str]]): Evaluate CRITERIA to filter photos.
*   `query_function` (Optional[List[str]]): Run function to filter photos.
*   `deleted_only` (bool): Include only photos from the 'Recently Deleted' folder.
*   `deleted` (bool): Include photos from the 'Recently Deleted' folder.
*   `add_to_album` (Optional[str]): Add all photos from query to album ALBUM in Photos.
*   `quiet` (bool): Quiet output; doesn't actually print query results.
*   `field` (Optional[List[str]]): Output only specified custom fields.
*   `print_template` (Optional[List[str]]): Render TEMPLATE string for each photo queried and print to stdout.
*   `mute` (bool): Mute status output while loading Photos library.

#### `show`

Shows photo, album, or folder in Photos from UUID_OR_NAME.

Invokes the `osxphotos show` command.

**Parameters:**
*   `uuid_or_name` (str): UUID or name of the photo, album, or folder.
*   `library` (Optional[str]): Specify path to Photos library.

#### `sync`

Syncs metadata and albums between Photos libraries.

Invokes the `osxphotos sync` command.

**Parameters:**
*   `export_file` (Optional[str]): Export metadata to file EXPORT_FILE.
*   `import_path` (Optional[str]): Import metadata from file IMPORT_PATH.
*   `set_metadata` (Optional[List[str]]): Set metadata in local Photos library to match import data.
*   `merge_metadata` (Optional[List[str]]): Merge metadata in local Photos library with import data.
*   `unmatched` (bool): Print out a list of photos in the import source that were not matched.
*   `report` (Optional[str]): Write a report of all photos that were processed with --import.
*   `append` (bool): If used with --report, add data to existing report file.
*   `dry_run` (bool): Dry run; when used with --import, don't actually update metadata.
*   `verbose` (bool): Print verbose output.
*   `timestamp` (bool): Add time stamp to verbose output.
*   `keyword` (Optional[List[str]]): Search for photos with keyword.
*   `no_keyword` (bool): Search for photos with no keyword.
*   `person` (Optional[List[str]]): Search for photos with person.
*   `album` (Optional[List[str]]): Search for photos in album.
*   `folder` (Optional[List[str]]): Search for photos in an album in folder.
*   `name` (Optional[List[str]]): Search for photos with filename matching.
*   `uuid` (Optional[List[str]]): Search for photos with UUID(s).
*   `uuid_from_file` (Optional[str]): Search for photos with UUID(s) loaded from FILE.
*   `title` (Optional[str]): Search for TITLE in title of photo.
*   `no_title` (bool): Search for photos with no title.
*   `description` (Optional[str]): Search for DESC in description of photo.
*   `no_description` (bool): Search for photos with no description.
*   `place` (Optional[str]): Search for PLACE in photo's reverse geolocation info.
*   `no_place` (bool): Search for photos with no associated place name info.
*   `location` (bool): Search for photos with associated location info.
*   `no_location` (bool): Search for photos with no associated location info.
*   `label` (Optional[List[str]]): Search for photos with image classification label.
*   `uti` (Optional[str]): Search for photos whose uniform type identifier (UTI) matches.
*   `ignore_case` (bool): Case insensitive search.
*   `edited` (bool): Search for photos that have been edited.
*   `not_edited` (bool): Search for photos that have not been edited.
*   `external_edit` (bool): Search for photos edited in external editor.
*   `favorite` (bool): Search for photos marked favorite.
*   `not_favorite` (bool): Search for photos not marked favorite.
*   `hidden` (bool): Search for photos marked hidden.
*   `not_hidden` (bool): Search for photos not marked hidden.
*   `burst` (bool): Search for photos that were taken in a burst.
*   `not_burst` (bool): Search for photos that are not part of a burst.
*   `live` (bool): Search for Apple live photos.
*   `not_live` (bool): Search for photos that are not Apple live photos.
*   `portrait` (bool): Search for Apple portrait mode photos.
*   `not_portrait` (bool): Search for photos that are not Apple portrait mode photos.
*   `screenshot` (bool): Search for screenshot photos.
*   `not_screenshot` (bool): Search for photos that are not screenshot photos.
*   `screen_recording` (bool): Search for screen-recording videos.
*   `not_screen_recording` (bool): Search for photos that are not screen recording videos.
*   `slow_mo` (bool): Search for slow motion videos.
*   `not_slow_mo` (bool): Search for photos that are not slow motion videos.
*   `time_lapse` (bool): Search for time lapse videos.
*   `not_time_lapse` (bool): Search for photos that are not time lapse videos.
*   `hdr` (bool): Search for high dynamic range (HDR) photos.
*   `not_hdr` (bool): Search for photos that are not HDR photos.
*   `selfie` (bool): Search for selfies.
*   `not_selfie` (bool): Search for photos that are not selfies.
*   `panorama` (bool): Search for panorama photos.
*   `not_panorama` (bool): Search for photos that are not panoramas.
*   `has_raw` (bool): Search for photos with both a jpeg and raw version.
*   `only_movies` (bool): Search only for movies.
*   `only_photos` (bool): Search only for photos/images.
*   `from_date` (Optional[str]): Search for items created on or after DATE.
*   `to_date` (Optional[str]): Search for items created before DATE.
*   `from_time` (Optional[str]): Search for items created on or after TIME of day.
*   `to_time` (Optional[str]): Search for items created before TIME of day.
*   `year` (Optional[List[int]]): Search for items from a specific year.
*   `added_before` (Optional[str]): Search for items added to the library before a specific date/time.
*   `added_after` (Optional[str]): Search for items added to the library on or after a specific date/time.
*   `added_in_last` (Optional[str]): Search for items added to the library in the last TIME_DELTA.
*   `has_comment` (bool): Search for photos that have comments.
*   `no_comment` (bool): Search for photos with no comments.
*   `has_likes` (bool): Search for photos that have likes.
*   `no_likes` (bool): Search for photos with no likes.
*   `is_reference` (bool): Search for photos that were imported as referenced files.
*   `not_reference` (bool): Search for photos that are not references.
*   `in_album` (bool): Search for photos that are in one or more albums.
*   `not_in_album` (bool): Search for photos that are not in any albums.
*   `duplicate` (bool): Search for photos with possible duplicates.
*   `min_size` (Optional[str]): Search for photos with size >= SIZE bytes.
*   `max_size` (Optional[str]): Search for photos with size <= SIZE bytes.
*   `missing` (bool): Search for photos missing from disk.
*   `not_missing` (bool): Search for photos present on disk.
*   `cloudasset` (bool): Search for photos that are part of an iCloud library.
*   `not_cloudasset` (bool): Search for photos that are not part of an iCloud library.
*   `incloud` (bool): Search for photos that are in iCloud.
*   `not_incloud` (bool): Search for photos that are not in iCloud.
*   `syndicated` (bool): Search for photos that have been shared via syndication.
*   `not_syndicated` (bool): Search for photos that have not been shared via syndication.
*   `saved_to_library` (bool): Search for syndicated photos that have saved to the library.
*   `not_saved_to_library` (bool): Search for syndicated photos that have not saved to the library.
*   `shared_moment` (bool): Search for photos that are part of a shared moment.
*   `not_shared_moment` (bool): Search for photos that are not part of a shared moment.
*   `shared_library` (bool): Search for photos that are part of a shared library.
*   `not_shared_library` (bool): Search for photos that are not part of a shared library.
*   `regex` (Optional[List[str]]): Search for photos where TEMPLATE matches regular expression REGEX.
*   `selected` (bool): Filter for photos that are currently selected in Photos.
*   `exif` (Optional[List[str]]): Search for photos where EXIF_TAG exists in photo's EXIF data and contains VALUE.
*   `query_eval` (Optional[List[str]]): Evaluate CRITERIA to filter photos.
*   `query_function` (Optional[List[str]]): Run function to filter photos.
*   `library` (Optional[str]): Specify path to Photos library.
*   `theme` (Optional[Literal['dark', 'light', 'mono', 'plain']]): Specify the color theme to use for output.

#### `timewarp`

Adjusts date/time/timezone of photos in Apple Photos.

Invokes the `osxphotos timewarp` command.

**Parameters:**
*   `date` (Optional[str]): Set date for selected photos.
*   `date_delta` (Optional[str]): Adjust date for selected photos by DELTA.
*   `time` (Optional[str]): Set time for selected photos.
*   `time_delta` (Optional[str]): Adjust time for selected photos by DELTA time.
*   `timezone` (Optional[str]): Set timezone for selected photos.
*   `date_added` (Optional[str]): Set date/time added for selected photos.
*   `date_added_from_photo` (bool): Set date/time added for selected photos to the date/time the photo was taken.
*   `reset` (bool): Reset date/time/timezone for selected photos to the original values.
*   `inspect` (bool): Print out the date/time/timezone for each selected photo without changing any information.
*   `compare_exif` (bool): Compare the EXIF date/time/timezone for each selected photo to the same data in Photos.
*   `push_exif` (bool): Push date/time and timezone for selected photos from Photos to the EXIF metadata.
*   `pull_exif` (bool): Pull date/time and timezone for selected photos from EXIF metadata.
*   `parse_date` (Optional[str]): Parse date from filename using DATE_PATTERN.
*   `function` (Optional[str]): Run python function to determine the date/time/timezone to apply to a photo.
*   `match_time` (bool): When used with --timezone, adjusts the photo time so that the timestamp in the new timezone matches the timestamp in the old timezone.
*   `use_file_time` (bool): When used with --pull-exif, the file modification date/time will be used if date/time is missing from the EXIF data.
*   `add_to_album` (Optional[str]): When used with --compare-exif, adds any photos with date/time/timezone differences to album ALBUM.
*   `uuid` (Optional[List[str]]): Apply to photo(s) with UUID(s).
*   `uuid_from_file` (Optional[str]): Apply to photos with UUID(s) loaded from FILE.
*   `verbose` (bool): Print verbose output.
*   `timestamp` (bool): Add time stamp to verbose output.
*   `library` (Optional[str]): Path to Photos library.
*   `exiftool_path` (Optional[str]): Optional path to exiftool executable.
*   `theme` (Optional[Literal['dark', 'light', 'mono', 'plain']]): Specify the color theme to use for output.
*   `plain` (bool): Plain text mode.
*   `force` (bool): Bypass confirmation prompt.

#### `tutorial`

Displays osxphotos tutorial.

Invokes the `osxphotos tutorial` command.

**Parameters:**
*   `width` (Optional[int]): Width of the tutorial output.

#### `update`

Updates the installation to the latest version.

Invokes the `osxphotos update` command.

**Parameters:** None

#### `uuid`

Prints out unique IDs (UUID) of photos selected in Photos.

Invokes the `osxphotos uuid` command.

**Parameters:**
*   `filename` (bool): Include filename of selected photos in output.

#### `version`

Checks for new version of osxphotos.

Invokes the `osxphotos version` command.

**Parameters:**

#### `install`

Installs Python packages into the same environment as osxphotos.

Invokes the `osxphotos install` command.

**Parameters:**

- `packages` (Optional[List[str]]): One or more package names to install.
- `upgrade` (bool): Upgrade packages to latest version.
- `requirements_file` (Optional[str]): Install from requirements file.

#### `run`

Runs a Python file using the same environment as osxphotos.

Invokes the `osxphotos run` command.

**Parameters:**

- `python_file` (str): Path or URL to the Python file to run.
- `args` (Optional[List[str]]): Additional arguments passed to the Python file.

#### `uninstall`

Uninstalls Python packages from the osxphotos environment.

Invokes the `osxphotos uninstall` command.

**Parameters:**

- `packages` (List[str]): One or more package names to uninstall.
- `yes` (bool): Don't ask for confirmation.

### Notes on interactive commands

The osxphotos commands `inspect` and `repl` are intentionally not exposed as MCP tools because they require interactive terminal control and real-time user interaction with Photos or a shell session. MCP tools run as single, stateless invocations and return outputs, which is not compatible with the continuous interactive behavior expected by these commands. If you need their functionality:

- For `inspect`, run it in a local terminal while using Photos for interactive selection.
- For `repl`, open the REPL in a terminal for exploratory work, then script repeatable logic and run it via the `run` tool.
*   `run` (Optional[str]): Run COMMAND if there is a new version of osxphotos available.

### How it Works

The tools in this server are wrappers around the `osxphotos` CLI tool. When you call a tool, the server constructs and executes the corresponding `osxphotos` command with the provided parameters. The output of the command is then returned to the client.

### Extending the Server

You can easily extend the server by adding new tools or modifying the existing ones in the `main.py` file.

To add a new tool, simply define a new function and decorate it with `@mcp.tool()`. The function's name will be the tool's name, and its parameters will be the tool's parameters. Inside the function, you can use the `subprocess` module to execute any `osxphotos` command you want.
