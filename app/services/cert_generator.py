import csv, os, shutil
from PIL import Image, ImageFont, ImageDraw
from reportlab.pdfgen import canvas

DEFAULTS = {
    "FONT_COLOR_DARK": "#000000",
    "FONT_COLOR_LIGHT": "#FFFFFF",
}

def textsize(draw, text, font):
    bbox = draw.textbbox((0, 0), text=text, font=font)
    return bbox[2]-bbox[0], bbox[3]-bbox[1]

def wrap_lines(text, max_len=57):
    words, lines, line = text.split(), [], ""
    for w in words:
        if len((line + " " + w).strip()) <= max_len:
            line = (line + " " + w).strip()
        else:
            lines.append(line); line = w
    if line: lines.append(line)
    return lines

def generate_single(
    name, description, title, subtitle, signer,
    template_path, output_dir,
    logo_path=None, sign_path=None,
    fonts={}
):
    im = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(im)

    font_big  = fonts.get("name", ImageFont.truetype("static/font/GreatVibes-Regular.ttf", 180))
    font_h3   = fonts.get("title", ImageFont.truetype("static/font/lemonmilk.otf", 55))
    font_sub  = fonts.get("subtitle", ImageFont.truetype("static/font/font4.ttf", 50))
    font_desc = fonts.get("desc", ImageFont.truetype("static/font/font4.ttf", 60))
    font_sign = fonts.get("signer", ImageFont.truetype("static/font/Poppins-Light.otf", 50))

    # pick font color by template index (1,5,6,7 => dark)
    font_color = DEFAULTS["FONT_COLOR_DARK"] if any(x in template_path for x in ["template1", "template5", "template6", "template7"]) else DEFAULTS["FONT_COLOR_LIGHT"]

    # Name
    w, h = textsize(draw, name, font_big)
    draw.text(((im.width - w)/2, (im.height - h)/2 - 30), name, fill=font_color, font=font_big)

    # Title
    w, h = textsize(draw, title, font_h3)
    draw.text(((im.width - w)/2, (im.height - h)/2 - 320), title, fill=font_color, font=font_h3)

    # Subtitle
    w, h = textsize(draw, subtitle, font_sub)
    draw.text(((im.width - w)/2, (im.height - h)/2 - 200), subtitle, fill=(255,215,0), font=font_sub)

    # Description (wrapped)
    y = (im.height)/2 + 145
    for line in wrap_lines(description, 57):
        w, h = textsize(draw, line, font_desc)
        draw.text(((im.width - w)/2, y), line, fill=font_color, font=font_desc)
        y += 80

    # Center logo
    if logo_path:
        overlay = Image.open(logo_path).convert("RGBA")
    else:
        overlay = None
    if overlay:
        nw = 400
        nh = int(overlay.height * (nw/overlay.width))
        overlay = overlay.resize((nw, nh), Image.LANCZOS)
        im.alpha_composite(overlay, ((im.width - nw)//2, 100))

    # Signature image
    if sign_path:
        sig = Image.open(sign_path).convert("RGBA")
        nw = 200; nh = int(sig.height * (nw/sig.width))
        sig = sig.resize((nw, nh), Image.LANCZOS)
        im.alpha_composite(sig, ((im.width - nw)//2, im.height - nh - 215))

    # Signer name
    w, h = textsize(draw, signer, font_sign)
    draw.text(((im.width - w)/2, im.height - h - 155), signer, fill=font_color, font=font_sign)

    # Save PNG then PDF
    os.makedirs(output_dir, exist_ok=True)
    png_path = os.path.join(output_dir, f"{name}.png")
    im.convert("RGB").save(png_path)

    pdf_path = os.path.join(output_dir, f"{name}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=im.size)
    c.drawImage(png_path, 0, 0, width=im.width, height=im.height, preserveAspectRatio=True)
    c.save()
    os.remove(png_path)

    return pdf_path

def generate_bulk(csv_path, template_path, output_dir):
    rows = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for r in reader:
            if r: rows.append(r[:5])  # [name, description, title, subtitle, signer]
    for name, desc, title, subtitle, signer in rows:
        generate_single(name, desc, title, subtitle, signer, template_path, output_dir)
    return len(rows)
