# Pixel Manipulation Image Encryption Tool

A beginner-friendly Django project that encrypts and decrypts images using two reversible pixel manipulation methods.

## Features

- Upload JPG or PNG images in the browser
- Encrypt or decrypt with the same numeric key
- Choose between two reversible methods:
  - `swap`: shuffle pixel positions with a seeded permutation
  - `math`: apply modular arithmetic to pixel values
- Preview the original and processed images side by side
- Download the processed result as a PNG
- Keep the image-processing logic modular in separate Python files

## Project Structure

- `manage.py` - Django command entry point
- `config/` - Django project settings and URLs
- `webapp/` - forms, views, template, and styling for the browser UI
- `encrypt.py` - encryption logic
- `decrypt.py` - decryption logic
- `utils.py` - shared helper functions
- `requirements.txt` - project dependencies

## Installation

1. Make sure Python 3 is installed.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run The Project

Start the Django development server:

```bash
python manage.py runserver
```

Then open your browser at:

```text
http://127.0.0.1:8000/
```

## How To Use

1. Upload a JPG or PNG image.
2. Enter a numeric key such as `42`.
3. Choose the method:
   - `swap` for seeded pixel shuffling
   - `math` for modular pixel changes
4. Choose the action:
   - `encrypt` to scramble the image
   - `decrypt` to reverse an earlier encrypted image
5. Click `Run Processing`.
6. Review the original and processed previews.
7. Download the processed PNG file.

## Important Notes

- Decryption only works correctly when you use the same key and the same method that were used during encryption.
- If you use the wrong key, the output image will still be created, but it will not match the original.
- Downloaded results are saved as PNG files to preserve pixel values exactly.
- PNG input is recommended when you want the cleanest reversible result.

## Sample Test Usage

Try this quick manual test in the browser:

1. Run `python manage.py runserver`.
2. Upload a PNG image.
3. Enter key `42`.
4. Choose action `encrypt` and method `swap`.
5. Submit the form and download the processed image.
6. Upload that processed image again.
7. Enter the same key `42`.
8. Choose action `decrypt` and method `swap`.
9. Submit the form and confirm the preview matches the original image.

Repeat the same flow with method `math`.
