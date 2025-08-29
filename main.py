import os
import sys
import shutil
import subprocess
import json
from mcp.server.fastmcp import FastMCP
from typing import List, Optional, Literal

mcp = FastMCP("mcp-osxphotos")

_resolved_osxphotos_path: Optional[str] = None

def resolve_osxphotos_path() -> str:
    """Resolve the path to the osxphotos executable.

    Resolution order:
    1. OSXPHOTOS_BIN environment variable (must be an executable file)
    2. System PATH via shutil.which("osxphotos")
    Caches the result for subsequent calls.
    """
    global _resolved_osxphotos_path
    if _resolved_osxphotos_path:
        return _resolved_osxphotos_path

    env_path = os.environ.get("OSXPHOTOS_BIN")
    if env_path and os.path.isfile(env_path) and os.access(env_path, os.X_OK):
        _resolved_osxphotos_path = env_path
        return _resolved_osxphotos_path

    which_path = shutil.which("osxphotos")
    if which_path:
        _resolved_osxphotos_path = which_path
        return _resolved_osxphotos_path

    raise FileNotFoundError(
        "Could not find 'osxphotos'. Set OSXPHOTOS_BIN to the executable path or add it to PATH."
    )

def run_osxphotos_command(command: List[str]) -> str:
    """Helper function to run an osxphotos command and return the output."""
    try:
        # Replace the binary name with the resolved absolute path when needed
        bin_path = resolve_osxphotos_path()
        cmd = list(command)
        if cmd and cmd[0] == "osxphotos":
            cmd[0] = bin_path
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except FileNotFoundError as e:
        return (
            "Error: osxphotos executable not found. "
            "Set OSXPHOTOS_BIN or update PATH. Details: " + str(e)
        )
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

@mcp.tool()
def osxphotos_health() -> str:
    """Return diagnostic info about how the server finds and runs osxphotos."""
    info = {"found": False}
    try:
        path = resolve_osxphotos_path()
        info.update({
            "found": True,
            "path": path,
            "env_OSXPHOTOS_BIN": os.environ.get("OSXPHOTOS_BIN"),
            "PATH": os.environ.get("PATH"),
        })
        # Try to get version
        out = subprocess.run([path, "--version"], capture_output=True, text=True, check=True)
        info["version"] = out.stdout.strip()
    except Exception as e:
        info["error"] = str(e)
    return json.dumps(info)

@mcp.tool()
def python_version() -> str:
    """Return the Python version used by this MCP server runtime."""
    return json.dumps({
        "version": sys.version,
        "executable": sys.executable,
    })

@mcp.tool()
def about() -> str:
    """Print information about osxphotos including license."""
    return run_osxphotos_command(["osxphotos", "about"])

@mcp.tool()
def add_locations(
    window: Optional[str] = None,
    dry_run: bool = False,
    verbose: bool = False,
    timestamp: bool = False,
    keyword: Optional[List[str]] = None,
    no_keyword: bool = False,
    person: Optional[List[str]] = None,
    album: Optional[List[str]] = None,
    folder: Optional[List[str]] = None,
    name: Optional[List[str]] = None,
    uuid: Optional[List[str]] = None,
    uuid_from_file: Optional[str] = None,
    title: Optional[str] = None,
    no_title: bool = False,
    description: Optional[str] = None,
    no_description: bool = False,
    place: Optional[str] = None,
    no_place: bool = False,
    location: bool = False,
    no_location: bool = False,
    label: Optional[List[str]] = None,
    uti: Optional[str] = None,
    ignore_case: bool = False,
    edited: bool = False,
    not_edited: bool = False,
    external_edit: bool = False,
    favorite: bool = False,
    not_favorite: bool = False,
    hidden: bool = False,
    not_hidden: bool = False,
    shared: bool = False,
    not_shared: bool = False,
    burst: bool = False,
    not_burst: bool = False,
    live: bool = False,
    not_live: bool = False,
    portrait: bool = False,
    not_portrait: bool = False,
    screenshot: bool = False,
    not_screenshot: bool = False,
    screen_recording: bool = False,
    not_screen_recording: bool = False,
    slow_mo: bool = False,
    not_slow_mo: bool = False,
    time_lapse: bool = False,
    not_time_lapse: bool = False,
    hdr: bool = False,
    not_hdr: bool = False,
    selfie: bool = False,
    not_selfie: bool = False,
    panorama: bool = False,
    not_panorama: bool = False,
    has_raw: bool = False,
    only_movies: bool = False,
    only_photos: bool = False,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    from_time: Optional[str] = None,
    to_time: Optional[str] = None,
    year: Optional[List[int]] = None,
    added_before: Optional[str] = None,
    added_after: Optional[str] = None,
    added_in_last: Optional[str] = None,
    has_comment: bool = False,
    no_comment: bool = False,
    has_likes: bool = False,
    no_likes: bool = False,
    is_reference: bool = False,
    not_reference: bool = False,
    in_album: bool = False,
    not_in_album: bool = False,
    duplicate: bool = False,
    min_size: Optional[str] = None,
    max_size: Optional[str] = None,
    missing: bool = False,
    not_missing: bool = False,
    cloudasset: bool = False,
    not_cloudasset: bool = False,
    incloud: bool = False,
    not_incloud: bool = False,
    syndicated: bool = False,
    not_syndicated: bool = False,
    saved_to_library: bool = False,
    not_saved_to_library: bool = False,
    shared_moment: bool = False,
    not_shared_moment: bool = False,
    shared_library: bool = False,
    not_shared_library: bool = False,
    regex: Optional[List[str]] = None,
    selected: bool = False,
    exif: Optional[List[str]] = None,
    query_eval: Optional[List[str]] = None,
    query_function: Optional[List[str]] = None,
    theme: Optional[Literal['dark', 'light', 'mono', 'plain']] = None,
) -> str:
    """Add missing location data to photos in Photos.app using nearest neighbor."""
    cmd = ["osxphotos", "add-locations"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def albums(
    library: Optional[str] = None,
    json: bool = False,
) -> str:
    """Print out albums found in the Photos library."""
    cmd = ["osxphotos", "albums"]
    if library:
        cmd.extend(["--library", library])
    if json:
        cmd.append("--json")
    return run_osxphotos_command(cmd)

@mcp.tool()
def batch_edit(
    title: Optional[str] = None,
    description: Optional[str] = None,
    keyword: Optional[List[str]] = None,
    replace_keywords: bool = False,
    location: Optional[List[float]] = None,
    album: Optional[List[str]] = None,
    split_folder: Optional[str] = None,
    dry_run: bool = False,
    undo: bool = False,
    verbose: bool = False,
    timestamp: bool = False,
    theme: Optional[Literal['dark', 'light', 'mono', 'plain']] = None,
    library: Optional[str] = None,
) -> str:
    """Batch edit photo metadata such as title, description, keywords, etc."""
    cmd = ["osxphotos", "batch-edit"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def compare(
    library_a: str,
    library_b: str,
    check: bool = False,
    csv: bool = False,
    tsv: bool = False,
    json: bool = False,
    output: Optional[str] = None,
    signature: Optional[str] = None,
    verbose: bool = False,
) -> str:
    """Compare two Photos libraries to find differences."""
    cmd = ["osxphotos", "compare", library_a, library_b]
    for key, value in locals().items():
        if key in ['library_a', 'library_b']:
            continue
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def docs() -> str:
    """Open osxphotos documentation in your browser."""
    return run_osxphotos_command(["osxphotos", "docs"])

@mcp.tool()
def dump(
    library: Optional[str] = None,
    json: bool = False,
    deleted_only: bool = False,
    deleted: bool = False,
    field: Optional[List[str]] = None,
    print_template: Optional[List[str]] = None,
) -> str:
    """DEPRECATED: Print list of all photos & associated info from the Photos library. Use query instead."""
    cmd = ["osxphotos", "dump"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def exiftool(
    export_directory: str,
    db_config: bool = False,
    load_config: Optional[str] = None,
    save_config: Optional[str] = None,
    exiftool_path: Optional[str] = None,
    exiftool_option: Optional[List[str]] = None,
    exiftool_merge_keywords: bool = False,
    exiftool_merge_persons: bool = False,
    ignore_date_modified: bool = False,
    person_keyword: bool = False,
    album_keyword: bool = False,
    keyword_template: Optional[List[str]] = None,
    replace_keywords: bool = False,
    description_template: Optional[str] = None,
    exportdb: Optional[str] = None,
    report: Optional[str] = None,
    append: bool = False,
    verbose: bool = False,
    timestamp: bool = False,
    dry_run: bool = False,
    theme: Optional[Literal['dark', 'light', 'mono', 'plain']] = None,
    library: Optional[str] = None,
) -> str:
    """Run exiftool on previously exported files to update metadata."""
    cmd = ["osxphotos", "exiftool", export_directory]
    for key, value in locals().items():
        if key == 'export_directory':
            continue
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def export_photos(
    dest: str,
    library: Optional[str] = None,
    verbose: bool = False,
    timestamp: bool = False,
    no_progress: bool = False,
    keyword: Optional[List[str]] = None,
    no_keyword: bool = False,
    person: Optional[List[str]] = None,
    album: Optional[List[str]] = None,
    folder: Optional[List[str]] = None,
    name: Optional[List[str]] = None,
    uuid: Optional[List[str]] = None,
    uuid_from_file: Optional[str] = None,
    title: Optional[str] = None,
    no_title: bool = False,
    description: Optional[str] = None,
    no_description: bool = False,
    place: Optional[str] = None,
    no_place: bool = False,
    location: bool = False,
    no_location: bool = False,
    label: Optional[List[str]] = None,
    uti: Optional[str] = None,
    ignore_case: bool = False,
    edited: bool = False,
    not_edited: bool = False,
    external_edit: bool = False,
    favorite: bool = False,
    not_favorite: bool = False,
    hidden: bool = False,
    not_hidden: bool = False,
    shared: bool = False,
    not_shared: bool = False,
    burst: bool = False,
    not_burst: bool = False,
    live: bool = False,
    not_live: bool = False,
    portrait: bool = False,
    not_portrait: bool = False,
    screenshot: bool = False,
    not_screenshot: bool = False,
    screen_recording: bool = False,
    not_screen_recording: bool = False,
    slow_mo: bool = False,
    not_slow_mo: bool = False,
    time_lapse: bool = False,
    not_time_lapse: bool = False,
    hdr: bool = False,
    not_hdr: bool = False,
    selfie: bool = False,
    not_selfie: bool = False,
    panorama: bool = False,
    not_panorama: bool = False,
    has_raw: bool = False,
    only_movies: bool = False,
    only_photos: bool = False,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    from_time: Optional[str] = None,
    to_time: Optional[str] = None,
    year: Optional[List[int]] = None,
    added_before: Optional[str] = None,
    added_after: Optional[str] = None,
    added_in_last: Optional[str] = None,
    has_comment: bool = False,
    no_comment: bool = False,
    has_likes: bool = False,
    no_likes: bool = False,
    is_reference: bool = False,
    not_reference: bool = False,
    in_album: bool = False,
    not_in_album: bool = False,
    duplicate: bool = False,
    min_size: Optional[str] = None,
    max_size: Optional[str] = None,
    missing: bool = False,
    not_missing: bool = False,
    cloudasset: bool = False,
    not_cloudasset: bool = False,
    incloud: bool = False,
    not_incloud: bool = False,
    syndicated: bool = False,
    not_syndicated: bool = False,
    saved_to_library: bool = False,
    not_saved_to_library: bool = False,
    shared_moment: bool = False,
    not_shared_moment: bool = False,
    shared_library: bool = False,
    not_shared_library: bool = False,
    regex: Optional[List[str]] = None,
    selected: bool = False,
    exif: Optional[List[str]] = None,
    query_eval: Optional[List[str]] = None,
    query_function: Optional[List[str]] = None,
    deleted_only: bool = False,
    deleted: bool = False,
    update: bool = False,
    force_update: bool = False,
    update_errors: bool = False,
    ignore_signature: bool = False,
    only_new: bool = False,
    limit: Optional[int] = None,
    dry_run: bool = False,
    export_as_hardlink: bool = False,
    touch_file: bool = False,
    overwrite: bool = False,
    retry: Optional[int] = None,
    export_by_date: bool = False,
    skip_edited: bool = False,
    skip_original_if_edited: bool = False,
    skip_bursts: bool = False,
    skip_live: bool = False,
    skip_raw: bool = False,
    skip_uuid: Optional[List[str]] = None,
    skip_uuid_from_file: Optional[str] = None,
    current_name: bool = False,
    convert_to_jpeg: bool = False,
    jpeg_quality: Optional[float] = None,
    fix_orientation: bool = False,
    preview: bool = False,
    preview_if_missing: bool = False,
    preview_suffix: Optional[str] = None,
    download_missing: bool = False,
    export_aae: bool = False,
    sidecar: Optional[Literal['xmp', 'json', 'exiftool']] = None,
    sidecar_drop_ext: bool = False,
    sidecar_template: Optional[List[str]] = None,
    exiftool_flag: bool = False,
    exiftool_path: Optional[str] = None,
    exiftool_option: Optional[List[str]] = None,
    exiftool_merge_keywords: bool = False,
    exiftool_merge_persons: bool = False,
    favorite_rating: bool = False,
    ignore_date_modified: bool = False,
    person_keyword: bool = False,
    album_keyword: bool = False,
    keyword_template: Optional[List[str]] = None,
    replace_keywords: bool = False,
    description_template: Optional[str] = None,
    finder_tag_template: Optional[List[str]] = None,
    finder_tag_keywords: bool = False,
    xattr_template: Optional[List[str]] = None,
    directory: Optional[str] = None,
    filename: Optional[str] = None,
    jpeg_ext: Optional[str] = None,
    strip: bool = False,
    edited_suffix: Optional[str] = None,
    original_suffix: Optional[str] = None,
    use_photos_export: bool = False,
    use_photokit: bool = False,
    report: Optional[str] = None,
    append: bool = False,
    cleanup: bool = False,
    keep: Optional[List[str]] = None,
    add_exported_to_album: Optional[str] = None,
    add_skipped_to_album: Optional[str] = None,
    add_missing_to_album: Optional[str] = None,
    post_command: Optional[List[str]] = None,
    post_command_error: Optional[Literal['continue', 'break']] = None,
    post_function: Optional[List[str]] = None,
    exportdb: Optional[str] = None,
    ramdb: bool = False,
    checkpoint: Optional[int] = None,
    ignore_exportdb: bool = False,
    no_exportdb: bool = False,
    tmpdir: Optional[str] = None,
    alt_copy: bool = False,
    alt_db: Optional[str] = None,
    load_config: Optional[str] = None,
    save_config: Optional[str] = None,
    config_only: bool = False,
    print_template: Optional[List[str]] = None,
    theme: Optional[Literal['dark', 'light', 'mono', 'plain']] = None,
) -> str:
    """Export photos from the Photos database."""
    cmd = ["osxphotos", "export", dest]
    for key, value in locals().items():
        if key == 'dest':
            continue
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def exportdb(
    export_database: str,
    version: bool = False,
    vacuum: bool = False,
    create: Optional[str] = None,
    check_signatures: bool = False,
    update_signatures: bool = False,
    touch_file: bool = False,
    runs: bool = False,
    last_run: bool = False,
    last_export_dir: bool = False,
    save_config: Optional[str] = None,
    info: Optional[str] = None,
    errors: bool = False,
    last_errors: bool = False,
    uuid_files: Optional[str] = None,
    uuid_info: Optional[str] = None,
    history: Optional[str] = None,
    delete_uuid: Optional[str] = None,
    delete_file: Optional[str] = None,
    report: Optional[List[str]] = None,
    upgrade: bool = False,
    check: bool = False,
    repair: bool = False,
    sql: Optional[str] = None,
    migrate_photos_library: Optional[str] = None,
    export_dir: Optional[str] = None,
    append: bool = False,
    verbose: bool = False,
    timestamp: bool = False,
    theme: Optional[Literal['dark', 'light', 'mono', 'plain']] = None,
    dry_run: bool = False,
) -> str:
    """Utilities for working with the osxphotos export database."""
    cmd = ["osxphotos", "exportdb", export_database]
    for key, value in locals().items():
        if key == 'export_database':
            continue
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def help_command(command: Optional[str] = None) -> str:
    """Print help; for help on commands: help <command>."""
    cmd = ["osxphotos", "help"]
    if command:
        cmd.append(command)
    return run_osxphotos_command(cmd)

@mcp.tool()
def import_photos(
    files_or_dirs: List[str],
    album: Optional[List[str]] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    keyword: Optional[List[str]] = None,
    merge_keywords: bool = False,
    location: Optional[List[float]] = None,
    favorite_rating: Optional[int] = None,
    auto_live: bool = False,
    parse_date: Optional[str] = None,
    parse_folder_date: Optional[str] = None,
    clear_metadata: bool = False,
    clear_location: bool = False,
    timezone: Optional[str] = None,
    exiftool: bool = False,
    exiftool_path: Optional[str] = None,
    sidecar: bool = False,
    sidecar_filename: Optional[str] = None,
    edited_suffix: Optional[str] = None,
    sidecar_ignore_date: bool = False,
    set_timezone: bool = False,
    exportdb: Optional[str] = None,
    exportdir: Optional[str] = None,
    relative_to: Optional[str] = None,
    dup_check: bool = False,
    skip_dups: bool = False,
    signature: Optional[str] = None,
    dup_albums: bool = False,
    split_folder: Optional[str] = None,
    walk: bool = False,
    glob: Optional[List[str]] = None,
    check: bool = False,
    check_not: bool = False,
    dry_run: bool = False,
    report: Optional[str] = None,
    resume: bool = False,
    append: bool = False,
    verbose: bool = False,
    timestamp: bool = False,
    no_progress: bool = False,
    check_templates: bool = False,
    post_function: Optional[List[str]] = None,
    stop_on_error: Optional[int] = None,
    force: bool = False,
    library: Optional[str] = None,
    theme: Optional[Literal['dark', 'light', 'mono', 'plain']] = None,
) -> str:
    """Import photos and videos into Photos."""
    cmd = ["osxphotos", "import"] + files_or_dirs
    for key, value in locals().items():
        if key == 'files_or_dirs':
            continue
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def info(
    library: Optional[str] = None,
    json: bool = False,
    verbose: bool = False,
) -> str:
    """Print out descriptive info of the Photos library database."""
    cmd = ["osxphotos", "info"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def keywords(
    library: Optional[str] = None,
    json: bool = False,
) -> str:
    """Print out keywords found in the Photos library."""
    cmd = ["osxphotos", "keywords"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def labels(
    library: Optional[str] = None,
    json: bool = False,
) -> str:
    """Print out image classification labels found in the Photos library."""
    cmd = ["osxphotos", "labels"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def list_libraries(
    json: bool = False,
) -> str:
    """Print list of Photos libraries found on the system."""
    cmd = ["osxphotos", "list"]
    if json:
        cmd.append("--json")
    return run_osxphotos_command(cmd)

@mcp.tool()
def orphans(
    export: Optional[str] = None,
    library: Optional[str] = None,
    verbose: bool = False,
    timestamp: bool = False,
    theme: Optional[Literal['dark', 'light', 'mono', 'plain']] = None,
) -> str:
    """Find orphaned photos in a Photos library."""
    cmd = ["osxphotos", "orphans"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def persons(
    library: Optional[str] = None,
    json: bool = False,
) -> str:
    """Print out persons (faces) found in the Photos library."""
    cmd = ["osxphotos", "persons"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def places(
    library: Optional[str] = None,
    json: bool = False,
) -> str:
    """Print out places found in the Photos library."""
    cmd = ["osxphotos", "places"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def push_exif(
    metadata: str,
    push_edited: bool = False,
    exiftool_path: Optional[str] = None,
    exiftool_option: Optional[List[str]] = None,
    exiftool_merge_keywords: bool = False,
    exiftool_merge_persons: bool = False,
    favorite_rating: bool = False,
    ignore_date_modified: bool = False,
    person_keyword: bool = False,
    album_keyword: bool = False,
    keyword_template: Optional[List[str]] = None,
    replace_keywords: bool = False,
    description_template: Optional[str] = None,
    report: Optional[str] = None,
    append: bool = False,
    compare: bool = False,
    dry_run: bool = False,
    verbose: bool = False,
    timestamp: bool = False,
    theme: Optional[Literal['dark', 'light', 'mono', 'plain']] = None,
    library: Optional[str] = None,
    keyword: Optional[List[str]] = None,
    no_keyword: bool = False,
    person: Optional[List[str]] = None,
    album: Optional[List[str]] = None,
    folder: Optional[List[str]] = None,
    name: Optional[List[str]] = None,
    uuid: Optional[List[str]] = None,
    uuid_from_file: Optional[str] = None,
    title: Optional[str] = None,
    no_title: bool = False,
    description: Optional[str] = None,
    no_description: bool = False,
    place: Optional[str] = None,
    no_place: bool = False,
    location: bool = False,
    no_location: bool = False,
    label: Optional[List[str]] = None,
    uti: Optional[str] = None,
    ignore_case: bool = False,
    edited: bool = False,
    not_edited: bool = False,
    external_edit: bool = False,
    favorite: bool = False,
    not_favorite: bool = False,
    hidden: bool = False,
    not_hidden: bool = False,
    shared: bool = False,
    not_shared: bool = False,
    burst: bool = False,
    not_burst: bool = False,
    live: bool = False,
    not_live: bool = False,
    portrait: bool = False,
    not_portrait: bool = False,
    screenshot: bool = False,
    not_screenshot: bool = False,
    screen_recording: bool = False,
    not_screen_recording: bool = False,
    slow_mo: bool = False,
    not_slow_mo: bool = False,
    time_lapse: bool = False,
    not_time_lapse: bool = False,
    hdr: bool = False,
    not_hdr: bool = False,
    selfie: bool = False,
    not_selfie: bool = False,
    panorama: bool = False,
    not_panorama: bool = False,
    has_raw: bool = False,
    only_movies: bool = False,
    only_photos: bool = False,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    from_time: Optional[str] = None,
    to_time: Optional[str] = None,
    year: Optional[List[int]] = None,
    added_before: Optional[str] = None,
    added_after: Optional[str] = None,
    added_in_last: Optional[str] = None,
    has_comment: bool = False,
    no_comment: bool = False,
    has_likes: bool = False,
    no_likes: bool = False,
    is_reference: bool = False,
    not_reference: bool = False,
    in_album: bool = False,
    not_in_album: bool = False,
    duplicate: bool = False,
    min_size: Optional[str] = None,
    max_size: Optional[str] = None,
    missing: bool = False,
    not_missing: bool = False,
    cloudasset: bool = False,
    not_cloudasset: bool = False,
    incloud: bool = False,
    not_incloud: bool = False,
    syndicated: bool = False,
    not_syndicated: bool = False,
    saved_to_library: bool = False,
    not_saved_to_library: bool = False,
    shared_moment: bool = False,
    not_shared_moment: bool = False,
    shared_library: bool = False,
    not_shared_library: bool = False,
    regex: Optional[List[str]] = None,
    selected: bool = False,
    exif: Optional[List[str]] = None,
    query_eval: Optional[List[str]] = None,
    query_function: Optional[List[str]] = None,
) -> str:
    """Write photo metadata to original files in the Photos library."""
    cmd = ["osxphotos", "push-exif", metadata]
    for key, value in locals().items():
        if key == 'metadata':
            continue
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def query_photos(
    library: Optional[str] = None,
    json: bool = False,
    count: bool = False,
    keyword: Optional[List[str]] = None,
    no_keyword: bool = False,
    person: Optional[List[str]] = None,
    album: Optional[List[str]] = None,
    folder: Optional[List[str]] = None,
    name: Optional[List[str]] = None,
    uuid: Optional[List[str]] = None,
    uuid_from_file: Optional[str] = None,
    title: Optional[str] = None,
    no_title: bool = False,
    description: Optional[str] = None,
    no_description: bool = False,
    place: Optional[str] = None,
    no_place: bool = False,
    location: bool = False,
    no_location: bool = False,
    label: Optional[List[str]] = None,
    uti: Optional[str] = None,
    ignore_case: bool = False,
    edited: bool = False,
    not_edited: bool = False,
    external_edit: bool = False,
    favorite: bool = False,
    not_favorite: bool = False,
    hidden: bool = False,
    not_hidden: bool = False,
    shared: bool = False,
    not_shared: bool = False,
    burst: bool = False,
    not_burst: bool = False,
    live: bool = False,
    not_live: bool = False,
    portrait: bool = False,
    not_portrait: bool = False,
    screenshot: bool = False,
    not_screenshot: bool = False,
    screen_recording: bool = False,
    not_screen_recording: bool = False,
    slow_mo: bool = False,
    not_slow_mo: bool = False,
    time_lapse: bool = False,
    not_time_lapse: bool = False,
    hdr: bool = False,
    not_hdr: bool = False,
    selfie: bool = False,
    not_selfie: bool = False,
    panorama: bool = False,
    not_panorama: bool = False,
    has_raw: bool = False,
    only_movies: bool = False,
    only_photos: bool = False,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    from_time: Optional[str] = None,
    to_time: Optional[str] = None,
    year: Optional[List[int]] = None,
    added_before: Optional[str] = None,
    added_after: Optional[str] = None,
    added_in_last: Optional[str] = None,
    has_comment: bool = False,
    no_comment: bool = False,
    has_likes: bool = False,
    no_likes: bool = False,
    is_reference: bool = False,
    not_reference: bool = False,
    in_album: bool = False,
    not_in_album: bool = False,
    duplicate: bool = False,
    min_size: Optional[str] = None,
    max_size: Optional[str] = None,
    missing: bool = False,
    not_missing: bool = False,
    cloudasset: bool = False,
    not_cloudasset: bool = False,
    incloud: bool = False,
    not_incloud: bool = False,
    syndicated: bool = False,
    not_syndicated: bool = False,
    saved_to_library: bool = False,
    not_saved_to_library: bool = False,
    shared_moment: bool = False,
    not_shared_moment: bool = False,
    shared_library: bool = False,
    not_shared_library: bool = False,
    regex: Optional[List[str]] = None,
    selected: bool = False,
    exif: Optional[List[str]] = None,
    query_eval: Optional[List[str]] = None,
    query_function: Optional[List[str]] = None,
    deleted_only: bool = False,
    deleted: bool = False,
    add_to_album: Optional[str] = None,
    quiet: bool = False,
    field: Optional[List[str]] = None,
    print_template: Optional[List[str]] = None,
    mute: bool = False,
) -> str:
    """Query the Photos database using 1 or more search options."""
    cmd = ["osxphotos", "query"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def show(uuid_or_name: str, library: Optional[str] = None) -> str:
    """Show photo, album, or folder in Photos from UUID_OR_NAME."""
    cmd = ["osxphotos", "show", uuid_or_name]
    if library:
        cmd.extend(["--library", library])
    return run_osxphotos_command(cmd)

@mcp.tool()
def sync(
    export_file: Optional[str] = None,
    import_path: Optional[str] = None,
    set_metadata: Optional[List[str]] = None,
    merge_metadata: Optional[List[str]] = None,
    unmatched: bool = False,
    report: Optional[str] = None,
    append: bool = False,
    dry_run: bool = False,
    verbose: bool = False,
    timestamp: bool = False,
    keyword: Optional[List[str]] = None,
    no_keyword: bool = False,
    person: Optional[List[str]] = None,
    album: Optional[List[str]] = None,
    folder: Optional[List[str]] = None,
    name: Optional[List[str]] = None,
    uuid: Optional[List[str]] = None,
    uuid_from_file: Optional[str] = None,
    title: Optional[str] = None,
    no_title: bool = False,
    description: Optional[str] = None,
    no_description: bool = False,
    place: Optional[str] = None,
    no_place: bool = False,
    location: bool = False,
    no_location: bool = False,
    label: Optional[List[str]] = None,
    uti: Optional[str] = None,
    ignore_case: bool = False,
    edited: bool = False,
    not_edited: bool = False,
    external_edit: bool = False,
    favorite: bool = False,
    not_favorite: bool = False,
    hidden: bool = False,
    not_hidden: bool = False,
    burst: bool = False,
    not_burst: bool = False,
    live: bool = False,
    not_live: bool = False,
    portrait: bool = False,
    not_portrait: bool = False,
    screenshot: bool = False,
    not_screenshot: bool = False,
    screen_recording: bool = False,
    not_screen_recording: bool = False,
    slow_mo: bool = False,
    not_slow_mo: bool = False,
    time_lapse: bool = False,
    not_time_lapse: bool = False,
    hdr: bool = False,
    not_hdr: bool = False,
    selfie: bool = False,
    not_selfie: bool = False,
    panorama: bool = False,
    not_panorama: bool = False,
    has_raw: bool = False,
    only_movies: bool = False,
    only_photos: bool = False,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    from_time: Optional[str] = None,
    to_time: Optional[str] = None,
    year: Optional[List[int]] = None,
    added_before: Optional[str] = None,
    added_after: Optional[str] = None,
    added_in_last: Optional[str] = None,
    has_comment: bool = False,
    no_comment: bool = False,
    has_likes: bool = False,
    no_likes: bool = False,
    is_reference: bool = False,
    not_reference: bool = False,
    in_album: bool = False,
    not_in_album: bool = False,
    duplicate: bool = False,
    min_size: Optional[str] = None,
    max_size: Optional[str] = None,
    missing: bool = False,
    not_missing: bool = False,
    cloudasset: bool = False,
    not_cloudasset: bool = False,
    incloud: bool = False,
    not_incloud: bool = False,
    syndicated: bool = False,
    not_syndicated: bool = False,
    saved_to_library: bool = False,
    not_saved_to_library: bool = False,
    shared_moment: bool = False,
    not_shared_moment: bool = False,
    shared_library: bool = False,
    not_shared_library: bool = False,
    regex: Optional[List[str]] = None,
    selected: bool = False,
    exif: Optional[List[str]] = None,
    query_eval: Optional[List[str]] = None,
    query_function: Optional[List[str]] = None,
    library: Optional[str] = None,
    theme: Optional[Literal['dark', 'light', 'mono', 'plain']] = None,
) -> str:
    """Sync metadata and albums between Photos libraries."""
    cmd = ["osxphotos", "sync"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def timewarp(
    date: Optional[str] = None,
    date_delta: Optional[str] = None,
    time: Optional[str] = None,
    time_delta: Optional[str] = None,
    timezone: Optional[str] = None,
    date_added: Optional[str] = None,
    date_added_from_photo: bool = False,
    reset: bool = False,
    inspect: bool = False,
    compare_exif: bool = False,
    push_exif: bool = False,
    pull_exif: bool = False,
    parse_date: Optional[str] = None,
    function: Optional[str] = None,
    match_time: bool = False,
    use_file_time: bool = False,
    add_to_album: Optional[str] = None,
    uuid: Optional[List[str]] = None,
    uuid_from_file: Optional[str] = None,
    verbose: bool = False,
    timestamp: bool = False,
    library: Optional[str] = None,
    exiftool_path: Optional[str] = None,
    theme: Optional[Literal['dark', 'light', 'mono', 'plain']] = None,
    plain: bool = False,
    force: bool = False,
) -> str:
    """Adjust date/time/timezone of photos in Apple Photos."""
    cmd = ["osxphotos", "timewarp"]
    for key, value in locals().items():
        if value:
            if isinstance(value, bool):
                cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
    return run_osxphotos_command(cmd)

@mcp.tool()
def tutorial(width: Optional[int] = None) -> str:
    """Display osxphotos tutorial."""
    cmd = ["osxphotos", "tutorial"]
    if width:
        cmd.append(str(width))
    return run_osxphotos_command(cmd)

@mcp.tool()
def update() -> str:
    """Update the installation to the latest version."""
    return run_osxphotos_command(["osxphotos", "update"])

@mcp.tool()
def uuid(filename: bool = False) -> str:
    """Print out unique IDs (UUID) of photos selected in Photos."""
    cmd = ["osxphotos", "uuid"]
    if filename:
        cmd.append("--filename")
    return run_osxphotos_command(cmd)

@mcp.tool()
def version(run: Optional[str] = None) -> str:
    """Check for new version of osxphotos."""
    cmd = ["osxphotos", "version"]
    if run:
        cmd.extend(["--run", run])
    return run_osxphotos_command(cmd)


@mcp.tool()
def install(
    packages: Optional[List[str]] = None,
    upgrade: bool = False,
    requirements_file: Optional[str] = None,
) -> str:
    """Install Python packages into the same environment as osxphotos."""
    cmd = ["osxphotos", "install"]
    if upgrade:
        cmd.append("--upgrade")
    if requirements_file:
        cmd.extend(["-r", requirements_file])
    if packages:
        cmd.extend(packages)
    return run_osxphotos_command(cmd)


@mcp.tool()
def run(
    python_file: str,
    args: Optional[List[str]] = None,
) -> str:
    """Run a python file using the same environment as osxphotos."""
    cmd = ["osxphotos", "run", python_file]
    if args:
        cmd.extend(args)
    return run_osxphotos_command(cmd)


@mcp.tool()
def uninstall(
    packages: List[str],
    yes: bool = False,
) -> str:
    """Uninstall Python packages from the osxphotos environment."""
    cmd = ["osxphotos", "uninstall"]
    if yes:
        cmd.append("--yes")
    cmd.extend(packages)
    return run_osxphotos_command(cmd)