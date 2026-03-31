"""Forms for the Pixel Manipulation Image Encryption Tool web app."""

from __future__ import annotations

from django import forms

from utils import validate_numeric_key, validate_supported_extension


METHOD_CHOICES = [
    ("swap", "Swap pixel positions"),
    ("math", "Math operation on pixel values"),
]

ACTION_CHOICES = [
    ("encrypt", "Encrypt image"),
    ("decrypt", "Decrypt image"),
]


class ImageProcessForm(forms.Form):
    """Collect the information required to encrypt or decrypt an image."""

    image = forms.ImageField(
        label="Image file",
        help_text="Upload a JPG or PNG image.",
    )
    key = forms.CharField(
        label="Numeric key",
        help_text="Use the same numeric key to reverse the operation later.",
        max_length=30,
    )
    method = forms.ChoiceField(
        label="Method",
        choices=METHOD_CHOICES,
        initial="swap",
    )
    action = forms.ChoiceField(
        label="Action",
        choices=ACTION_CHOICES,
        initial="encrypt",
    )

    def clean_key(self) -> int:
        """Convert the submitted key into an integer."""
        return validate_numeric_key(self.cleaned_data["key"])

    def clean_image(self):
        """Reject unsupported file extensions before processing."""
        uploaded_image = self.cleaned_data["image"]
        validate_supported_extension(uploaded_image.name)
        return uploaded_image
