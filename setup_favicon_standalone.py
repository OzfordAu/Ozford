# Run this with:
#   python manage.py shell < setup_favicon_standalone.py
#
# (manage.py shell already sets up Django using your project's normal
# settings, so this script just needs to be plain Python — no folders,
# no __init__.py files, no management command.)

import os
from PIL import Image
from django.conf import settings
from django.core.management import call_command
from site_settings.models import SiteSettings

# 1. Get the logo file from Wagtail (footer_logo — the flat navy OIHE mark)
site_settings = SiteSettings.objects.live().first() or SiteSettings.objects.first()
if not site_settings or not site_settings.footer_logo:
    raise SystemExit(
        "Could not find SiteSettings.footer_logo. Is the page published "
        "and does it have a Footer Logo set in the Wagtail admin?"
    )

logo_path = site_settings.footer_logo.file.path
print(f"Using logo: {logo_path}")

# 2. Prepare output dir
static_dir = os.path.join(settings.BASE_DIR, "core", "static", "favicons")
os.makedirs(static_dir, exist_ok=True)

# 3. Load logo. This image is a flat rectangle (navy bg baked in already,
# no transparency), so we letterbox it onto a square canvas using its own
# corner pixel as the background color, instead of compositing white-on-transparent.
logo = Image.open(logo_path).convert("RGBA")
BG_COLOR = logo.getpixel((2, 2))  # sample background from a corner


def make_icon(size, padding_ratio=0.1):
    bg = Image.new("RGBA", (size, size), BG_COLOR)
    pad = int(size * padding_ratio)
    inner = size - 2 * pad
    logo_resized = logo.copy()
    logo_resized.thumbnail((inner, inner), Image.LANCZOS)
    x = (size - logo_resized.width) // 2
    y = (size - logo_resized.height) // 2
    bg.paste(logo_resized, (x, y), logo_resized)
    return bg.convert("RGB")


sizes = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "favicon-48x48.png": 48,
    "apple-touch-icon.png": 180,
    "android-chrome-192x192.png": 192,
    "android-chrome-512x512.png": 512,
}

generated = {}
for filename, size in sizes.items():
    img = make_icon(size)
    path = os.path.join(static_dir, filename)
    img.save(path)
    generated[size] = img
    print(f"Generated {filename}")

# .ico bundle (16/32/48)
ico_path = os.path.join(static_dir, "favicon.ico")
generated[16].save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
print("Generated favicon.ico")

# 4. site.webmanifest
manifest_path = os.path.join(static_dir, "site.webmanifest")
with open(manifest_path, "w") as f:
    f.write(
        '{\n'
        '  "name": "Ozford Institute of Higher Education",\n'
        '  "short_name": "OIHE",\n'
        '  "icons": [\n'
        '    {"src": "/static/favicons/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},\n'
        '    {"src": "/static/favicons/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}\n'
        '  ],\n'
        '  "theme_color": "#1D315A",\n'
        '  "background_color": "#1D315A",\n'
        '  "display": "standalone"\n'
        '}\n'
    )
print("Generated site.webmanifest")

# 5. Update base.html (idempotent)
base_html_path = os.path.join(settings.BASE_DIR, "core", "templates", "base.html")
with open(base_html_path, "r") as f:
    content = f.read()

marker = '<link rel="icon" type="image/x-icon"'
if marker in content:
    print("base.html already has favicon tags — skipping edit.")
else:
    anchor = '<link rel="canonical" href="{{ page.get_full_url }}" />'
    favicon_tags = (
        '\n        <link rel="icon" type="image/x-icon" href="{% static \'favicons/favicon.ico\' %}">\n'
        '        <link rel="icon" type="image/png" sizes="16x16" href="{% static \'favicons/favicon-16x16.png\' %}">\n'
        '        <link rel="icon" type="image/png" sizes="32x32" href="{% static \'favicons/favicon-32x32.png\' %}">\n'
        '        <link rel="apple-touch-icon" sizes="180x180" href="{% static \'favicons/apple-touch-icon.png\' %}">\n'
        '        <link rel="manifest" href="{% static \'favicons/site.webmanifest\' %}">\n'
        '        <meta name="theme-color" content="#1D315A">'
    )
    if anchor not in content:
        print(
            "Could not find the expected anchor line in base.html. "
            "Favicon files were generated, but you'll need to add the <link> tags manually."
        )
    else:
        content = content.replace(anchor, anchor + favicon_tags, 1)
        with open(base_html_path, "w") as f:
            f.write(content)
        print("base.html updated with favicon tags.")

# 6. collectstatic
print("Running collectstatic...")
call_command("collectstatic", "--noinput")
print("\nAll done! Hard-refresh your browser (Ctrl+Shift+R) to see the favicon.")
