"""Decryption logic for the Pixel Manipulation Image Encryption Tool."""

from __future__ import annotations

from collections.abc import Callable

from PIL import Image

from utils import build_image_from_pixels, build_permutation, subtract_value_from_pixel


ProgressCallback = Callable[[int, str], None]


def decrypt_image(
    image: Image.Image,
    key: int,
    method: str,
    progress_callback: ProgressCallback | None = None,
) -> Image.Image:
    """Decrypt an image with the selected method."""
    method_name = method.lower().strip()
    if method_name == "swap":
        return decrypt_with_swap(image, key, progress_callback)
    if method_name == "math":
        return decrypt_with_math(image, key, progress_callback)

    raise ValueError("Unsupported decryption method. Choose 'swap' or 'math'.")


def decrypt_with_swap(
    image: Image.Image,
    key: int,
    progress_callback: ProgressCallback | None = None,
) -> Image.Image:
    """Restore the original pixel order using the same seed key."""
    pixels = list(image.getdata())
    total_pixels = len(pixels)
    permutation = build_permutation(total_pixels, key)

    restored_pixels: list[int | tuple[int, ...]] = [pixels[0]] * total_pixels

    for encrypted_index, original_index in enumerate(permutation):
        restored_pixels[original_index] = pixels[encrypted_index]
        maybe_report_loop_progress(
            index=encrypted_index,
            total=total_pixels,
            message="Restoring pixel positions...",
            progress_callback=progress_callback,
        )

    return build_image_from_pixels(restored_pixels, image.size, image.mode)


def decrypt_with_math(
    image: Image.Image,
    key: int,
    progress_callback: ProgressCallback | None = None,
) -> Image.Image:
    """Undo the math-based encryption on each pixel."""
    pixels = list(image.getdata())
    total_pixels = len(pixels)
    key_value = key % 256
    decrypted_pixels: list[int | tuple[int, ...]] = [pixels[0]] * total_pixels

    for index, pixel in enumerate(pixels):
        decrypted_pixels[index] = subtract_value_from_pixel(pixel, key_value)
        maybe_report_loop_progress(
            index=index,
            total=total_pixels,
            message="Reversing math encryption...",
            progress_callback=progress_callback,
        )

    return build_image_from_pixels(decrypted_pixels, image.size, image.mode)


def maybe_report_loop_progress(
    index: int,
    total: int,
    message: str,
    progress_callback: ProgressCallback | None,
) -> None:
    """Update progress roughly every 5 percent for smoother UI feedback."""
    if not progress_callback or total <= 0:
        return

    if index == total - 1:
        progress_callback(100, message)
        return

    step_size = max(1, total // 20)
    if index % step_size != 0:
        return

    percent = int(((index + 1) / total) * 100)
    progress_callback(percent, message)
