from flask import Blueprint, render_template, request, send_file, current_app, redirect, url_for, flash
import os, shutil
from .services.cert_generator import generate_single, generate_bulk
from .services.file_ops import ensure_dirs, empty_dir
from zipfile import ZipFile

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return render_template("home.html")

@bp.route("/generate", methods=["GET", "POST"])
def generate():
    cfg = current_app.config
    ensure_dirs(cfg["UPLOAD_FOLDER"], cfg["OUTPUT_DIR"])

    if request.method == "POST":
        template_index = request.form.get("template_index", "2")
        template_path  = f"{cfg['TEMPLATE_PREFIX']}{template_index}.png"

        # Single certificate (manual fields)
        if "mode" in request.form and request.form["mode"] == "single":
            name = request.form["name"]
            title = request.form["title"]
            subtitle = request.form["subtitle"]
            description = request.form["description"]
            signer = request.form["signer_name"]
            logo = request.files.get("logo")
            sign = request.files.get("sign")

            empty_dir(cfg["OUTPUT_DIR"])
            logo_path = os.path.join(cfg["UPLOAD_FOLDER"], "logo.png") if logo else None
            if logo: logo.save(logo_path)
            sign_path = os.path.join(cfg["UPLOAD_FOLDER"], "sign.png") if sign else None
            if sign: sign.save(sign_path)

            generate_single(name, description, title, subtitle, signer, template_path, cfg["OUTPUT_DIR"], logo_path, sign_path)
            zip_path = _zip_output(cfg["OUTPUT_DIR"])
            return redirect(url_for(".success", zip="1"))

        # Bulk via CSV
        if "file" in request.files:
            csv_file = request.files["file"]
            if csv_file.filename:
                empty_dir(cfg["OUTPUT_DIR"])
                csv_path = os.path.join(cfg["UPLOAD_FOLDER"], "names.csv")
                csv_file.save(csv_path)
                generate_bulk(csv_path, template_path, cfg["OUTPUT_DIR"])
                zip_path = _zip_output(cfg["OUTPUT_DIR"])
                return redirect(url_for(".success", zip="1"))

    return render_template("generate.html")

@bp.route("/success")
def success():
    return render_template("success.html")

@bp.route("/download")
def download():
    zip_path = os.path.join(current_app.config["OUTPUT_DIR"], "certificates.zip")
    return send_file(zip_path, as_attachment=True)

def _zip_output(outdir):
    zip_path = os.path.join(outdir, "certificates.zip")
    with ZipFile(zip_path, "w") as zf:
        for f in os.listdir(outdir):
            if f.endswith(".pdf"):
                zf.write(os.path.join(outdir, f), arcname=f)
    return zip_path
