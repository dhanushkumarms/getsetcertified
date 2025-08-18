from flask import Flask, redirect, render_template, request, send_file, url_for
from PIL import Image, ImageFont, ImageDraw
import csv
import os
import zipfile
from io import BytesIO
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Global Variables
FONT_FILE = ImageFont.truetype('static/font/GreatVibes-Regular.ttf', 180)
FONT_FILE2 = ImageFont.truetype('static/font/font4.ttf', 60)
FONT_FILE3 = ImageFont.truetype('static/font/lemonmilk.otf', 55)
FONT_FILE4 = ImageFont.truetype('static/font/font4.ttf', 50)
FONT_FILE5 = ImageFont.truetype('static/font/Poppins-Light.otf', 50)
FONT_COLOR = "#FFFFFF"
TEMPLATE_PATH = 'static/template2.png'
OUTPUT_DIR = 'static/out/'
OUTPUT_CERTIFICATE = 'static/outputcertificate/'


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    global FONT_COLOR
    global TEMPLATE_PATH
    if request.method == 'POST':
        if 'file' not in request.files and 'logo' not in request.files:
            return render_template('index.html', error='No file part')

        hidden_value = request.form['template_index']
        TEMPLATE_PATH = 'static/template' + hidden_value + '.png'

        FONT_COLOR = "#000000" if hidden_value in ['1', '5', '6', '7'] else "#FFFFFF"

        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return render_template('index.html', error='No selected file')
            csv_filename = 'names.csv'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], csv_filename))
            delete_everything_inside_directory(OUTPUT_DIR)
            generate_certificates(csv_filename)
            zip_path = create_zip()
            return render_template('index.html', zip_path=zip_path)

        if 'logo' in request.files:
            logo = request.files['logo']
            title = request.form['title']
            name = request.form['name']
            subtitle = request.form['subtitle']
            description = request.form['description']
            sign = request.files['sign']
            signer = request.form['signer_name']
            delete_everything_inside_directory(OUTPUT_DIR)
            make_certificate(name, description, title, subtitle, signer, logo, sign)
            zip_path = create_zip()
            return render_template('index.html', zip_path=zip_path)

    return render_template('index.html')


def delete_everything_inside_directory(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            delete_everything_inside_directory(item_path)
            os.rmdir(item_path)


def textsize(text, font):
    im = Image.new(mode="RGB", size=(0, 0))
    draw = ImageDraw.Draw(im)
    bbox = draw.textbbox((0, 0), text=text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height


def split_string_by_length(text, max_length):
    words = text.split()
    result = []
    current_part = ''
    for word in words:
        if len(current_part + ' ' + word) <= max_length:
            current_part += ' ' + word if current_part else word
        else:
            result.append(current_part.strip())
            current_part = word
    if current_part:
        result.append(current_part.strip())
    return result


def make_certificate(name, description, title, subtitle, signer, logo=None, sign=None):
    image_source = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(image_source)

    # Draw name, title, subtitle, and description
    name_width, name_height = textsize(name, FONT_FILE)
    draw.text(((image_source.width - name_width) / 2, (image_source.height - name_height) / 2 - 30), name, fill=FONT_COLOR, font=FONT_FILE)

    title_width, title_height = textsize(title, FONT_FILE3)
    draw.text(((image_source.width - title_width) / 2, (image_source.height - title_height) / 2 - 320), title, fill=FONT_COLOR, font=FONT_FILE3)

    subtitle_width, subtitle_height = textsize(subtitle, FONT_FILE4)
    draw.text(((image_source.width - subtitle_width) / 2, (image_source.height - subtitle_height) / 2 - 200), subtitle, fill=(255, 215, 0), font=FONT_FILE4)

    desc_lines = split_string_by_length(description, 57)
    y_offset = 0
    for line in desc_lines:
        desc_width, desc_height = textsize(line, FONT_FILE2)
        draw.text(((image_source.width - desc_width) / 2, (image_source.height - desc_height) / 2 + 145 + y_offset), line, fill=FONT_COLOR, font=FONT_FILE2)
        y_offset += 80

    # Add logo
    if logo:
        logo_image = Image.open(logo).convert("RGBA")
    else:
        logo_image = Image.open("overlay_image.png").convert("RGBA")
    logo_width = 400
    logo_scale = logo_width / float(logo_image.size[0])
    logo_height = int((float(logo_image.size[1]) * logo_scale))
    logo_image = logo_image.resize((logo_width, logo_height), Image.LANCZOS)
    logo_position = ((image_source.width - logo_image.width) // 2, 100)
    image_source.paste(logo_image, logo_position, logo_image)

    # Add signature
    if sign:
        sign_image = Image.open(sign).convert("RGBA")
    else:
        sign_image = Image.open("sign.png").convert("RGBA")
    sign_width = 200
    sign_scale = sign_width / float(sign_image.size[0])
    sign_height = int((float(sign_image.size[1]) * sign_scale))
    sign_image = sign_image.resize((sign_width, sign_height), Image.LANCZOS)
    sign_position = ((image_source.width - sign_image.width) // 2, (image_source.height - sign_image.height) - 215)
    image_source.paste(sign_image, sign_position, sign_image)

    # Signer name
    signer_width, signer_height = textsize(signer, FONT_FILE5)
    draw.text(((image_source.width - signer_width) / 2, (image_source.height - signer_height) - 155), signer, fill=FONT_COLOR, font=FONT_FILE5)

    # Save temporary PNG
    temp_png_path = os.path.join(OUTPUT_DIR, name + ".png")
    image_source.save(temp_png_path)

    # Save as PDF
    pdf_path = os.path.join(OUTPUT_DIR, name + ".pdf")
    image_width, image_height = image_source.size
    pdf = canvas.Canvas(pdf_path, pagesize=(image_width, image_height))
    pdf.drawImage(temp_png_path, 0, 0, width=image_width, height=image_height)
    pdf.save()

    os.remove(temp_png_path)
    print('Saved certificate for:', name)


def generate_certificates(csv_filename):
    data = read_data_from_csv(csv_filename)
    for row in data:
        make_certificate(*row)
    print(f"{len(data)} certificates generated.")


def read_data_from_csv(filename):
    data = []
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                data.append(row[:5])
    return data


def create_zip():
    zip_filename = 'certificates'
    zip_path = shutil.make_archive(OUTPUT_CERTIFICATE + zip_filename, 'zip', OUTPUT_DIR)
    return zip_path


@app.route('/download_zip')
def download_zip():
    zip_path = 'static/outputcertificate/certificates.zip'
    return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_CERTIFICATE, exist_ok=True)
    app.run(debug=True)
