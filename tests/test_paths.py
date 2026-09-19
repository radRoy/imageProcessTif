from pathlib import Path

from mesospim.io.paths import (
    add_filename_suffix,
    create_sibling_dir,
    ensure_dir,
    filter_by_extension,
    filter_by_substring,
    filter_by_unwanted_substring,
    generate_suffixed_output_paths,
    list_files,
    split_filename,
)


def test_ensure_dir(tmp_path: Path):
    target = tmp_path / "sub" / "nested"
    assert not target.exists()
    res = ensure_dir(target)
    assert res == target
    assert target.is_dir()


def test_create_sibling_dir(tmp_path: Path):
    base_dir = tmp_path / "input_data"
    base_dir.mkdir()

    sibling = create_sibling_dir(base_dir, "-processed")
    assert sibling.exists()
    assert sibling.is_dir()
    assert sibling.name == "input_data-processed"
    assert sibling.parent == tmp_path


def test_list_files(tmp_path: Path):
    (tmp_path / "file1.tif").write_text("dummy")
    (tmp_path / "file2.tiff").write_text("dummy")
    (tmp_path / "file3.h5").write_text("dummy")
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    (sub_dir / "nested.tif").write_text("dummy")

    # Flat listing
    all_flat = list_files(tmp_path)
    assert len(all_flat) == 3
    assert [p.name for p in all_flat] == ["file1.tif", "file2.tiff", "file3.h5"]

    # Filter by extension
    tif_files = list_files(tmp_path, extension=".tif")
    assert len(tif_files) == 1
    assert tif_files[0].name == "file1.tif"

    # Recursive listing
    recursive_tif = list_files(tmp_path, extension="tif", recursive=True)
    assert len(recursive_tif) == 2
    assert [p.name for p in recursive_tif] == ["file1.tif", "nested.tif"]


def test_filter_by_extension():
    paths = ["/a/b/c.tif", Path("/a/b/d.h5"), "/a/b/e.TIF", "/a/b/f.txt"]
    res = filter_by_extension(paths, ".tif")
    assert [p.name for p in res] == ["c.tif", "e.TIF"]

    res_no_dot = filter_by_extension(paths, "h5")
    assert [p.name for p in res_no_dot] == ["d.h5"]


def test_filter_by_substring():
    paths = ["id01-sample1.tif", "id02-sample2.tif", "id01-sample3.tif"]
    res = filter_by_substring(paths, "id01")
    assert [p.name for p in res] == ["id01-sample1.tif", "id01-sample3.tif"]

    res_exclude = filter_by_substring(paths, "id01", exclude=True)
    assert [p.name for p in res_exclude] == ["id02-sample2.tif"]


def test_filter_by_unwanted_substring():
    paths = ["sample_good.tif", "sample_bad_corrupted.tif", "another_good.tif"]
    res = filter_by_unwanted_substring(paths, "bad")
    assert [p.name for p in res] == ["sample_good.tif", "another_good.tif"]


def test_split_filename():
    stem, ext = split_filename("path/to/my_image.tif")
    assert stem == "my_image"
    assert ext == ".tif"


def test_add_filename_suffix():
    p = Path("/data/folder/stack.tif")
    out = add_filename_suffix(p, "-8bit")
    assert out == Path("/data/folder/stack-8bit.tif")

    # With extension replacement
    out_h5 = add_filename_suffix(p, "_raw", new_extension=".h5")
    assert out_h5 == Path("/data/folder/stack_raw.h5")


def test_generate_suffixed_output_paths(tmp_path: Path):
    inputs = [
        tmp_path / "raw" / "sample1.tif",
        tmp_path / "raw" / "sample2.tif",
    ]
    out_dir = tmp_path / "processed"

    # With output_dir
    outputs = generate_suffixed_output_paths(
        inputs,
        suffix="_normalized",
        output_dir=out_dir,
        new_extension="h5",
    )
    assert out_dir.is_dir()
    assert len(outputs) == 2
    assert outputs[0] == out_dir / "sample1_normalized.h5"
    assert outputs[1] == out_dir / "sample2_normalized.h5"

    # In-place (parent dir)
    outputs_inplace = generate_suffixed_output_paths(inputs, suffix="_8bit")
    assert outputs_inplace[0] == tmp_path / "raw" / "sample1_8bit.tif"
    assert outputs_inplace[1] == tmp_path / "raw" / "sample2_8bit.tif"
