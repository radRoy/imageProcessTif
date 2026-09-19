"""Headless, pure pathlib-based filesystem and path utilities."""

from collections.abc import Sequence
from pathlib import Path


def ensure_dir(path: Path | str) -> Path:
    """Create directory if it does not exist, including parent directories.

    Args:
        path: Directory path as Path object or string.

    Returns:
        Path object of the ensured directory.
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def create_sibling_dir(path: Path | str, suffix: str) -> Path:
    """Create a sibling directory adjacent to the given directory by appending a suffix.

    Args:
        path: Path to the base directory.
        suffix: Suffix to append to the base directory name.

    Returns:
        Path object pointing to the newly created sibling directory.
    """
    base_path = Path(path).resolve()
    # If a trailing slash was present or directory, name is the last component
    sibling_name = f"{base_path.name}{suffix}"
    sibling_path = base_path.parent / sibling_name
    sibling_path.mkdir(parents=True, exist_ok=True)
    return sibling_path


def list_files(
    directory: Path | str,
    pattern: str = "*",
    extension: str | None = None,
    recursive: bool = False,
    sort: bool = True,
) -> list[Path]:
    """List files in a directory matching an optional glob pattern and/or extension.

    Args:
        directory: Directory to search in.
        pattern: Glob pattern to match (default: "*").
        extension: Optional file extension to filter by (e.g., ".tif" or "tif").
        recursive: Whether to search recursively in subdirectories.
        sort: Whether to sort returned paths alphabetically.

    Returns:
        List of Path objects for all matching files.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        return []

    iterator = dir_path.rglob(pattern) if recursive else dir_path.glob(pattern)
    files = [p for p in iterator if p.is_file()]

    if extension is not None:
        ext = extension if extension.startswith(".") else f".{extension}"
        files = [p for p in files if p.suffix.lower() == ext.lower()]

    if sort:
        files.sort(key=lambda p: p.as_posix().lower())

    return files


def filter_by_extension(paths: Sequence[Path | str], extension: str) -> list[Path]:
    """Filter paths that end with a specific extension (case-insensitive).

    Args:
        paths: Sequence of file paths or string path names.
        extension: Extension to filter for (e.g. '.tif', 'tif', '.h5').

    Returns:
        List of Path objects matching the extension.
    """
    ext = extension if extension.startswith(".") else f".{extension}"
    ext_lower = ext.lower()
    return [Path(p) for p in paths if Path(p).suffix.lower() == ext_lower]


def filter_by_substring(
    paths: Sequence[Path | str],
    substring: str,
    exclude: bool = False,
) -> list[Path]:
    """Filter a sequence of paths by the presence or absence of a substring.

    Args:
        paths: Sequence of file paths or strings.
        substring: Substring to check for in the filename/path.
        exclude: If True, keep paths that do NOT contain the substring.
            If False, keep paths that DO contain the substring.

    Returns:
        Filtered list of Path objects.
    """
    if exclude:
        return [Path(p) for p in paths if substring not in Path(p).name]
    return [Path(p) for p in paths if substring in Path(p).name]


def filter_by_unwanted_substring(
    paths: Sequence[Path | str],
    substring: str,
) -> list[Path]:
    """Filter out paths containing the unwanted substring.

    Args:
        paths: Sequence of file paths or strings.
        substring: Substring that should NOT be in the filename.

    Returns:
        Filtered list of Path objects.
    """
    return filter_by_substring(paths, substring, exclude=True)


def split_filename(file_path: Path | str) -> tuple[str, str]:
    """Split a filename into its stem (name without extension) and suffix (extension).

    Args:
        file_path: File path or filename.

    Returns:
        Tuple of (stem, suffix), e.g., ("image_01", ".tif").
    """
    p = Path(file_path)
    return p.stem, p.suffix


def add_filename_suffix(
    file_path: Path | str,
    suffix: str,
    new_extension: str | None = None,
) -> Path:
    """Add a suffix to a file's name before its extension.

    Args:
        file_path: Path to the input file.
        suffix: Suffix string to append to the filename stem (e.g. '-8bit' or '_cropped').
        new_extension: Optional replacement extension (e.g. '.h5' or 'h5').
            If None, the existing extension is preserved.

    Returns:
        Path object with the updated filename in the same parent directory.
    """
    p = Path(file_path)
    ext = (
        p.suffix
        if new_extension is None
        else (new_extension if new_extension.startswith(".") else f".{new_extension}")
    )
    new_name = f"{p.stem}{suffix}{ext}"
    return p.parent / new_name


def generate_suffixed_output_paths(
    input_paths: Sequence[Path | str],
    suffix: str,
    output_dir: Path | str | None = None,
    new_extension: str | None = None,
) -> list[Path]:
    """Generate corresponding output paths for a list of input files by applying a suffix.

    Args:
        input_paths: Sequence of input file paths.
        suffix: Suffix to append to each filename stem.
        output_dir: Optional destination directory. If None, output paths will reside
            in the respective parent directories of the input files.
        new_extension: Optional new extension for output files.

    Returns:
        List of Path objects for the target output files.
    """
    out_dir_path = Path(output_dir) if output_dir is not None else None
    if out_dir_path is not None:
        out_dir_path.mkdir(parents=True, exist_ok=True)

    output_paths: list[Path] = []
    for inp in input_paths:
        suffixed_path = add_filename_suffix(inp, suffix, new_extension=new_extension)
        if out_dir_path is not None:
            output_paths.append(out_dir_path / suffixed_path.name)
        else:
            output_paths.append(suffixed_path)

    return output_paths
