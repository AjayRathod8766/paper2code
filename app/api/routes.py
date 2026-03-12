"""
app/api/routes.py
Flask REST API for Paper2Code — production ready with full CORS support.
"""

import os
import json
import traceback
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename

from app.logger.logger        import get_logger
from app.parser.pdf_parser    import PDFParser
from app.parser.text_cleaner  import TextCleaner
from app.extractor.info_extractor  import InfoExtractor
from app.generator.code_generator  import CodeGenerator
from config import OUTPUT_DIR

log       = get_logger(__name__)
bp        = Blueprint("api", __name__, url_prefix="/api")
cleaner   = TextCleaner()
extractor = InfoExtractor()
generator = CodeGenerator()

ALLOWED_EXT = {"pdf"}
MAX_FILE_MB = 20


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# ── POST /api/generate ────────────────────────────────────────
@bp.route("/generate", methods=["POST", "OPTIONS"])
def generate_from_pdf():
    if request.method == "OPTIONS":
        return _cors_preflight()

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Use key 'file'."}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "Empty filename."}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are supported."}), 400

    file.seek(0, 2)
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)
    if size_mb > MAX_FILE_MB:
        return jsonify({"error": f"File too large ({size_mb:.1f} MB). Max is {MAX_FILE_MB} MB."}), 400

    framework = request.form.get("framework", None)
    filename  = secure_filename(file.filename)
    tmp_path  = os.path.join(os.environ.get("TEMP", "C:\\Temp"), filename)

    try:
        file.save(tmp_path)
        log.info(f"PDF saved: {tmp_path} ({size_mb:.2f} MB)")
        result = _process_pipeline(tmp_path, framework=framework)
        return jsonify(result), 200
    except Exception as e:
        log.error(f"Pipeline error: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# ── POST /api/generate/text ───────────────────────────────────
@bp.route("/generate/text", methods=["POST", "OPTIONS"])
def generate_from_text():
    if request.method == "OPTIONS":
        return _cors_preflight()

    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify({"error": "JSON body with 'text' field required."}), 400

    try:
        clean_text = cleaner.clean(data["text"])
        info       = extractor.extract(clean_text)
        result     = generator.generate(info, framework=data.get("framework"))
        return jsonify({
            "status":   "success",
            "info":     result["info"],
            "filename": result["filename"],
            "code":     result["code"],
        }), 200
    except Exception as e:
        log.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# ── GET /api/outputs ──────────────────────────────────────────
@bp.route("/outputs", methods=["GET"])
def list_outputs():
    try:
        files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".py")]
        return jsonify({"count": len(files), "files": sorted(files, reverse=True)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── GET /api/outputs/<filename> ───────────────────────────────
@bp.route("/outputs/<filename>", methods=["GET"])
def download_output(filename):
    path = os.path.join(OUTPUT_DIR, secure_filename(filename))
    if not os.path.exists(path):
        return jsonify({"error": "File not found."}), 404
    return send_file(path, as_attachment=True, mimetype="text/plain")


# ── GET /api/health ───────────────────────────────────────────
@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Paper2Code API", "version": "1.0.0"}), 200


# ── Helpers ───────────────────────────────────────────────────
def _process_pipeline(pdf_path: str, framework: str = None) -> dict:
    log.info(f"Pipeline start: {pdf_path}")
    parser     = PDFParser(pdf_path)
    parsed     = parser.parse()
    clean_text = cleaner.clean(parsed["full_text"])
    info       = extractor.extract(clean_text)
    log.info(f"Extracted: {json.dumps(info, indent=2)}")
    result     = generator.generate(info, framework=framework)
    return {
        "status":    "success",
        "paper":     parsed["filename"],
        "num_pages": parsed["num_pages"],
        "info":      result["info"],
        "filename":  result["filename"],
        "code":      result["code"],
    }


def _cors_preflight():
    response = jsonify({"status": "ok"})
    response.status_code = 200
    return response
