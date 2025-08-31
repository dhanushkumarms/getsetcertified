class Config:
    # Flask settings
    SECRET_KEY = "dev-secret"   # change in production

    # File storage
    UPLOAD_FOLDER = "uploads"                 # where CSV uploads go
    OUTPUT_DIR = "certificates"               # where generated PDFs/ZIPs are stored
    TEMPLATE_PREFIX = "static/template"       # prefix path for template images

    # File limits (optional safeguard)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
