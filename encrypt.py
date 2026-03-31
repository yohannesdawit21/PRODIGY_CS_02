"""Encryption logic for the Pixel Manipulation Image Encryption Tool."""

from __future__ import annotations

from collections.abc import Callable

from PIL import Image

from utils import add_value_to_pixel, build_image_from_pixels, build_permutation


ProgressCallback = Callable[[int, str], None]


def encrypt_image(
    image: Image.Image,
    key: int,
    method: str,
    progress_callback: ProgressCallback | None = None,
) -> Image.Image:
    """Encrypt an image with the selected method."""
    method_name = method.lower().strip()
    if method_name == "swap":
        return encrypt_with_swap(image, key, progress_callback)
    if method_name == "math":
        return encrypt_with_math(image, key, progress_callback)

    raise ValueError("Unsupported encryption method. Choose 'swap' or 'math'.")


def encrypt_with_swap(
    image: Image.Image,
    key: int,
    progress_callback: ProgressCallback | None = None,
) -> Image.Image:
    """Encrypt by shuffling pixel positions with a seed key."""
    pixels = list(image.getdata())
    total_pixels = len(pixels)
    permutation = build_permutation(total_pixels, key)

    shuffled_pixels: list[int | tuple[int, ...]] = [pixels[0]] * total_pixels
    report_progress(progress_callback, 5, "Building shuffled pixel order...")

    for index, shuffled_index in enumerate(permutation):
        shuffled_pixels[index] = pixels[shuffled_index]
        maybe_report_loop_progress(
            index=index,
            total=total_pixels,
            start_percent=5,
            end_percent=100,
            message="Shuffling pixels...",
            progress_callback=progress_callback,
        )

    return build_image_from_pixels(shuffled_pixels, image.size, image.mode)


def encrypt_with_math(
    image: Image.Image,
    key: int,
    progress_callback: ProgressCallback | None = None,
) -> Image.Image:
    """Encrypt by changing each pixel value with modular arithmetic."""
    pixels = list(image.getdata())
    total_pixels = len(pixels)
    key_value = key % 256
    encrypted_pixels: list[int | tuple[int, ...]] = [pixels[0]] * total_pixels

    for index, pixel in enumerate(pixels):
        encrypted_pixels[index] = add_value_to_pixel(pixel, key_value)
        maybe_report_loop_progress(
            index=index,
            total=total_pixels,
            start_percent=0,
            end_percent=100,
            message="Applying math encryption...",
            progress_callback=progress_callback,
        )

    return build_image_from_pixels(encrypted_pixels, image.size, image.mode)


def report_progress(
    progress_callback: ProgressCallback | None,
    percent: int,
    message: str,
) -> None:
    """Send a progress update if the caller requested it."""
    if progress_callback:
        progress_callback(percent, message)


def maybe_report_loop_progress(
    index: int,
    total: int,
    start_percent: int,
    end_percent: int,
    message: str,
    progress_callback: ProgressCallback | None,
) -> None:
    """Update progress roughly every 5 percent for smoother UI feedback."""
    if not progress_callback or total <= 0:
        return

    if index == total - 1:
        progress_callback(end_percent, message)
        return

    step_size = max(1, total // 20)
    if index % step_size != 0:
        return

    completion = (index + 1) / total
    scaled_percent = start_percent + int((end_percent - start_percent) * completion)
    progress_callback(min(end_percent, scaled_percent), message)
