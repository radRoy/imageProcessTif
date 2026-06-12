#!/usr/bin/env python3
"""
Generate a Markdown file listing internal dependencies between Python files
in a software project.

- Uses AST for accurate import parsing (better than regex/grep)
- Distinguishes internal project modules from stdlib and common external libraries
- Produces both forward and reverse dependency views
- Excludes common virtualenv, cache, and build directories
- Easy to customize (KNOWN_EXTERNAL list, exclude patterns, etc.)

Usage:
    python list_internal_dependencies.py

Output: internal-dependencies.md in the current directory (project root recommended)
"""

import ast
import fnmatch
from collections import defaultdict
from pathlib import Path


def get_all_py_files(root: Path, exclude_patterns=None):
    """Find all .py files while excluding common non-source directories."""
    if exclude_patterns is None:
        exclude_patterns = [
            '**/venv/**', '**/env/**', '**/.venv/**',
            '**/site-packages/**', '**/__pycache__/**',
            '**/.git/**', '**/build/**', '**/dist/**',
            '**/node_modules/**', '**/.mypy_cache/**', '**/.pytest_cache/**'
        ]
    
    py_files = []
    for py_file in root.rglob('*.py'):
        rel_path = py_file.relative_to(root)
        if any(fnmatch.fnmatch(str(rel_path), pat) for pat in exclude_patterns):
            continue
        py_files.append(py_file)
    return py_files


def get_top_level_internals(py_files: list[Path], root: Path) -> set[str]:
    """Collect top-level module/package names that exist in the project."""
    tops = set()
    for pyf in py_files:
        rel = pyf.relative_to(root)
        if len(rel.parts) == 1:
            tops.add(rel.stem)          # e.g. main.py -> "main"
        else:
            tops.add(rel.parts[0])      # first directory or top package
    return tops


def extract_imports(filepath: Path) -> list[str]:
    """Parse a Python file with AST and return top-level imported module names."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            source = f.read()
        tree = ast.parse(source, filename=str(filepath))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return []
    
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mod = alias.name.split('.')[0]
                if mod:
                    imports.add(mod)

            # elif node.module:  # absolute import
            #     mod = node.module.split('.')[0]
            #     if mod:
            #         imports.add(mod)
        elif isinstance(node, ast.ImportFrom):
            if node.level > 0:
                # Relative import (from .foo import bar or from . import baz)
                # Prefer module name if available
                if node.module:
                    mod = node.module.split('.')[0]
                    if mod:
                        imports.add(mod)
                # Pure relative: from . import xxx, yyy
                # (The dot . probably means, import from the same directory as the file where the import statement was called from)
                else:
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])  # take top-level name
            # Absolute imports
            elif node.module:
                mod = node.module.split('.')[0]
                if mod:
                    imports.add(mod)
    return list(imports)


def is_likely_internal(
    module: str,
    top_level_internals: set[str],
    known_external: set[str]
) -> bool:
    """Decide whether an import is internal to this project."""
    if not module:
        return False
    if module in {'__future__', '__main__'}:
        return False
    if module in known_external:
        return False
    if module in top_level_internals:
        return True
    return False  # unknown third-party or stdlib not in our list -> treat as external for now


def main():
    project_root = Path.cwd().resolve()
    print(f"Scanning Python project in: {project_root}")

    py_files = get_all_py_files(project_root)
    print(f"Found {len(py_files)} Python source files after exclusions.")

    if not py_files:
        print("No Python files found. Exiting.")
        return

    top_level_internals = get_top_level_internals(py_files, project_root)

    # Comprehensive list of stdlib + very common third-party packages.
    # Add or remove items specific to your project as needed.
    KNOWN_EXTERNAL: set[str] = {
        # Standard library (selected common ones; Python has many more)
        'abc', 'argparse', 'ast', 'asyncio', 'base64', 'bisect', 'builtins',
        'collections', 'concurrent', 'configparser', 'contextlib', 'copy',
        'csv', 'datetime', 'difflib', 'dis', 'email', 'enum', 'fileinput',
        'fnmatch', 'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob',
        'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'importlib',
        'inspect', 'io', 'itertools', 'json', 'keyword', 'linecache', 'locale',
        'logging', 'lzma', 'mailbox', 'math', 'mimetypes', 'mmap', 'modulefinder',
        'multiprocessing', 'numbers', 'operator', 'optparse', 'os', 'pathlib',
        'pickle', 'pkgutil', 'platform', 'plistlib', 'pprint', 'profile',
        'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'queue', 'quopri',
        'random', 're', 'readline', 'reprlib', 'resource', 'rlcompleter',
        'runpy', 'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex',
        'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket',
        'socketserver', 'sqlite3', 'ssl', 'stat', 'statistics', 'string',
        'stringprep', 'struct', 'subprocess', 'sunau', 'symbol', 'symtable',
        'sys', 'sysconfig', 'tabnanny', 'tarfile', 'tempfile', 'termios',
        'textwrap', 'threading', 'time', 'timeit', 'token', 'tokenize',
        'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 'turtledemo',
        'types', 'typing', 'unicodedata', 'unittest', 'urllib', 'uu', 'uuid',
        'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg', 'winsound',
        'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile', 'zipimport',
        'zlib', 'zoneinfo',
        # Very common third-party packages (expand for your project)
        'numpy', 'pandas', 'matplotlib', 'scipy', 'scikit-learn', 'sklearn',
        'tensorflow', 'torch', 'requests', 'flask', 'django', 'fastapi',
        'sqlalchemy', 'pydantic', 'click', 'typer', 'rich', 'tqdm', 'pytest',
        'black', 'isort', 'mypy', 'ruff', 'poetry', 'pip', 'setuptools',
        'wheel', 'jupyter', 'notebook', 'ipython', 'PIL', 'Pillow', 'cv2',
        'wheel', 'jupyter', 'notebook', 'ipython', 'PIL', 'Pillow', 'cv2',
        'opencv-python', 'networkx', 'graphviz', 'seaborn', 'plotly',
        'streamlit', 'gradio', 'httpx', 'aiohttp', 'beautifulsoup4', 'bs4',
        'lxml', 'openpyxl', 'xlsxwriter', 'pyyaml', 'yaml', 'toml', 'tomli',
        'gitpython', 'docker', 'kubernetes', 'boto3', 'botocore', 'skimage',
    }

    file_to_imports: dict[Path, set[str]] = defaultdict(set)

    # Dictionary of file paths and the modules imported in said file
    for py_file in py_files:
        raw_imports = extract_imports(py_file)
        for imp in raw_imports:
            if is_likely_internal(imp, top_level_internals, KNOWN_EXTERNAL):
                file_to_imports[py_file].add(imp)

    # HIER STEHENGEBLIEBEN

    # Build reverse map (what depends on each module)
    reverse_deps: dict[str, set[str]] = defaultdict(set)
    for py_file, deps in file_to_imports.items():
        rel_file = str(py_file.relative_to(project_root))
        for dep in deps:
            reverse_deps[dep].add(rel_file)

    #
    # TBD: Add the Grok Cycle dependency detection code here (and check for related diffs in code above and below, too)
    #

    # Write nice Markdown report
    output_path = project_root / 'internal-dependencies.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('# Internal Project Dependencies\n\n')
        f.write(f'**Project root:** `{project_root}`\n')
        f.write(f'**Files scanned:** {len(py_files)}\n\n')
        f.write('> Generated by `list_internal_dependencies.py` using AST parsing.\n')
        f.write('> External libraries (stdlib + common third-party) are excluded.\n\n')

        # Forward dependencies
        f.write('## Files => Their Internal Dependencies\n\n')
        for py_file in sorted(py_files, key=lambda p: p.relative_to(project_root)):
            rel = py_file.relative_to(project_root)
            deps = sorted(file_to_imports.get(py_file, set()))
            f.write(f'### `{rel}`\n')
            if deps:
                for d in deps:
                    f.write(f'- `{d}`\n')
            else:
                f.write('- *(no internal dependencies detected)*\n')
            f.write('\n')

        # Reverse dependencies
        f.write('## Reverse View: What Depends on Each Module\n\n')
        f.write('*(Useful for understanding impact of changes)*\n\n')
        for mod in sorted(reverse_deps.keys()):
            users = sorted(reverse_deps[mod])
            f.write(f'### `{mod}`\n')
            f.write(f'Used by {len(users)} file(s):\n')
            for user in users:
                f.write(f'- `{user}`\n')
            f.write('\n')

        # Simple stats
        total_internal_refs = sum(len(d) for d in file_to_imports.values())
        f.write('## Summary Statistics\n\n')
        f.write(f'- Total internal dependency references: {total_internal_refs}\n')
        f.write(f'- Modules with the most dependents: (see reverse view above)\n')
        if reverse_deps:
            most_used = max(reverse_deps.items(), key=lambda x: len(x[1]))
            f.write(f'- Most depended-on module: `{most_used[0]}` (used by {len(most_used[1])} files)\n')

    print(f"\n✓ Dependency map written to: {output_path}")
    print("Open it in any Markdown viewer or editor for easy reading.")


if __name__ == '__main__':
    main()
