# 🏆 GetSetCertified – Online Certificate Generator

<p align="center">
  <img src="static/img/gsc_logo.png" width="500" alt="GetSetCertified Logo"/>
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


## 🛠 Tech Stack  
- **Backend:** Python, Flask  
- **Frontend:** HTML, Jinja2, TailwindCSS  
- **PDF Generation:** ReportLab  
- **File Handling:** CSV, ZIP  
- **Styling:** Custom fonts (Poppins, Great Vibes, Lemon Milk)  

# ⚙️ Installation & Setup  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/dhanushkumarms/getsetcertified.git
   cd getsetcertified
   ```

2. **Create and activate a virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate   # for Linux/Mac
   venv\Scripts\activate      # for Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**  
   ```bash
   python run.py
   ```

5. **Open in browser:**  
   ```
   http://127.0.0.1:5000
   ```

## 🚀 Usage
- Choose a template
- Enter details (or upload CSV for bulk)
- Upload logo & signature (optional)
- Generate and download certificates

## 🔮 Future Enhancements
- User authentication (save & manage certificates online)
- More template designs
- Cloud storage & sharing options
- API integration for third-party apps

## 📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

## 👨‍💻 Author
Dhanushkumar M S
