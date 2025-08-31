# 🏆 GetSetCertified – Online Certificate Generator

<p align="center">
  <img src="static/img/logo.svg" width="800" alt="GetSetCertified Logo"/>
</p>

[![GSC](https://img.shields.io/badge/GetSetCertified-ACTIVE-brightgreen?style=for-the-badge)](#)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-black?style=for-the-badge&logo=flask)
![Pillow](https://img.shields.io/badge/Pillow-orange?style=for-the-badge)
![ReportLab](https://img.shields.io/badge/ReportLab-red?style=for-the-badge)
![HTML](https://img.shields.io/badge/HTML-5-orange?style=for-the-badge)
![CSS](https://img.shields.io/badge/CSS-3-blue?style=for-the-badge)

## 📌 Description
Flask web app to generate beautiful certificates from a CSV or single form with logos, signatures, and multiple templates. Exports crisp PDFs and a ZIP bundle.

## ✨ Features
- Bulk CSV or single entry
- Multiple templates, custom fonts
- High-quality PDF export
- One-click ZIP download

## 📸 Screenshots
<p align="center">
  <img src="static/img/screenshots/template-picker.png" width="300"/>
  <img src="static/img/screenshots/single-generate.png" width="300"/>
  <img src="static/img/screenshots/bulk-generate.png" width="300"/>
</p>

## 🚀 Setup
```bash
git clone https://github.com/your-username/getsetcertified.git
cd getsetcertified
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
# http://127.0.0.1:5000
