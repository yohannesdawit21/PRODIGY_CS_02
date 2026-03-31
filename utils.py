"""Utility helpers for the Pixel Manipulation Image Encryption Tool."""

from __future__ import annotations

import base64
import random
from io import BytesIO
from pathlib import Path
from typing import Iterable

from PIL import Image


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def validate_numeric_key(key_text: str) -> int:
    """Convert the user input into an integer key.

    The same numeric key must be used for encryption and decryption.
    """
    cleaned_key = key_text.strip()
    if not cleaned_key:
        raise ValueError("Please enter a numeric key.")

    try:
        return int(cleaned_key)
    except ValueError as error:
        raise ValueError("The key must be a whole number.") from error


def validate_supported_extension(filename: str) -> str:
    """Check that the filename has a supported image extension."""
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError("Only JPG and PNG images are supported.")

    return suffix


def ensure_supported_file(file_path: str | Path) -> Path:
    """Check that the selected file exists and is a supported image type."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    validate_supported_extension(path.name)
    return path


def normalize_image_mode(image: Image.Image) -> Image.Image:
    """Convert unusual image modes into a format we can safely process."""
    if image.mode in {"L", "RGB", "RGBA"}:
        return image.copy()

    if "A" in image.getbands():
        return image.convert("RGBA")

    return image.convert("RGB")


def load_image(file_path: str | Path) -> Image.Image:
    """Load an image from disk and convert it to a supported mode."""
    path = ensure_supported_file(file_path)
    with Image.open(path) as image:
        return normalize_image_mode(image)


def load_image_from_bytes(image_bytes: bytes, filename: str) -> Image.Image:
    """Load an uploaded image directly from bytes."""
    validate_supported_extension(filename)
    with Image.open(BytesIO(image_bytes)) as image:
        return normalize_image_mode(image)


def save_image(image: Image.Image, file_path: str | Path) -> None:
    """Save an image to disk."""
    path = Path(file_path)
    if not path.parent.exists():
        raise FileNotFoundError("The destination folder does not exist.")

    output_image = image

    # JPEG does not support transparency, so convert RGBA images before saving.
    if path.suffix.lower() in {".jpg", ".jpeg"} and image.mode == "RGBA":
        output_image = image.convert("RGB")

    output_image.save(path)


def image_to_bytes(image: Image.Image, image_format: str = "PNG") -> bytes:
    """Convert a Pillow image into raw bytes."""
    byte_stream = BytesIO()

    output_image = image
    if image_format.upper() == "JPEG" and image.mode == "RGBA":
        output_image = image.convert("RGB")

    output_image.save(byte_stream, format=image_format)
    return byte_stream.getvalue()


def image_to_data_url(image: Image.Image, image_format: str = "PNG") -> str:
    """Convert a Pillow image into a browser-friendly data URL."""
    encoded_bytes = base64.b64encode(image_to_bytes(image, image_format)).decode("ascii")
    mime_type = "image/png" if image_format.upper() == "PNG" else "image/jpeg"
    return f"data:{mime_type};base64,{encoded_bytes}"


def build_permutation(pixel_count: int, seed_key: int) -> list[int]:
    """Build a deterministic shuffled list of pixel positions.

    Using the same seed key always produces the same order, which makes
    decryption possible later.
    """
    indices = list(range(pixel_count))
    random.Random(seed_key).shuffle(indices)
    return indices


def add_value_to_pixel(pixel: int | tuple[int, ...], key_value: int) -> int | tuple[int, ...]:
    """Apply the reversible math operation to a pixel."""
    if isinstance(pixel, int):
        return (pixel + key_value) % 256

    return tuple((channel + key_value) % 256 for channel in pixel)


def subtract_value_from_pixel(
    pixel: int | tuple[int, ...],
    key_value: int,
) -> int | tuple[int, ...]:
    """Undo the reversible math operation from a pixel."""
    if isinstance(pixel, int):
        return (pixel - key_value) % 256

    return tuple((channel - key_value) % 256 for channel in pixel)


def build_image_from_pixels(
    pixels: Iterable[int | tuple[int, ...]],
    size: tuple[int, int],
    mode: str,
) -> Image.Image:
    """Create a new Pillow image from pixel data."""
    output_image = Image.new(mode, size)
    output_image.putdata(list(pixels))
    return output_image
