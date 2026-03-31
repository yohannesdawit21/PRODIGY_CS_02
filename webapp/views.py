"""Views for the Pixel Manipulation Image Encryption Tool web app."""

from __future__ import annotations

from pathlib import Path

from django.shortcuts import render

from webapp.forms import ImageProcessForm
from webapp.services.decrypt import decrypt_image
from webapp.services.encrypt import encrypt_image
from webapp.services.utils import image_to_data_url, load_image_from_bytes


def index_view(request):
    """Display the upload form and process the image when submitted."""
    form = ImageProcessForm(request.POST or None, request.FILES or None)
    context = {
        "form": form,
        "result": None,
    }

    if request.method == "POST" and form.is_valid():
        uploaded_image = form.cleaned_data["image"]
        image_bytes = uploaded_image.read()
        original_image = load_image_from_bytes(image_bytes, uploaded_image.name)

        key = form.cleaned_data["key"]
        method = form.cleaned_data["method"]
        action = form.cleaned_data["action"]

        if action == "encrypt":
            processed_image = encrypt_image(original_image, key, method)
            action_label = "Encrypted"
        else:
            processed_image = decrypt_image(original_image, key, method)
            action_label = "Decrypted"

        filename_stem = Path(uploaded_image.name).stem
        download_name = f"{filename_stem}_{action}_{method}.png"

        context["result"] = {
            "action_label": action_label,
            "download_name": download_name,
            "input_name": uploaded_image.name,
            "image_mode": original_image.mode,
            "image_size": f"{original_image.width} x {original_image.height}",
            "method": method,
            "key": key,
            "method_label": dict(form.fields["method"].choices)[method],
            "action_value": action,
            "original_preview": image_to_data_url(original_image),
            "processed_preview": image_to_data_url(processed_image),
            "processed_download": image_to_data_url(processed_image),
        }

    return render(request, "webapp/index.html", context)
