"""
main.py — Entry point for Paper2Code

Usage:
  python main.py --server           → Start Flask API (port 5000)
  python main.py --pdf paper.pdf    → Run CLI mode
"""

import argparse
import json
import sys

from flask import Flask
from flask_cors import CORS

from app.logger.logger import get_logger
from app.api.routes    import bp as api_bp
from config            import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

log = get_logger("paper2code.main")


def create_app() -> Flask:
    app = Flask(__name__)

    # Allow requests from React dev server (port 3000) and any origin
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "*"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    app.register_blueprint(api_bp)

    # Add CORS headers to every response just in case
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"]  = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response

    return app


def run_cli(pdf_path: str, framework: str = None):
    from app.api.routes import _process_pipeline
    log.info(f"CLI mode — Processing: {pdf_path}")
    try:
        result = _process_pipeline(pdf_path, framework=framework)
        print("\n" + "=" * 60)
        print("  Paper2Code — Extraction Results")
        print("=" * 60)
        print(json.dumps(result["info"], indent=2))
        print(f"\n✅ Generated script: {result['filename']}")
        print(f"📁 Saved to:        outputs/{result['filename']}")
        print("=" * 60)
        print("\nFirst 25 lines of generated code:")
        print("─" * 60)
        for line in result["code"].split("\n")[:25]:
            print(line)
        print("─" * 60)
    except Exception as e:
        log.error(f"CLI failed: {e}")
        sys.exit(1)


def run_server():
    app = create_app()
    log.info("=" * 50)
    log.info(f"  Paper2Code API starting...")
    log.info(f"  URL: http://localhost:{FLASK_PORT}")
    log.info(f"  Endpoints:")
    log.info(f"    POST /api/generate       — Upload PDF")
    log.info(f"    POST /api/generate/text  — Send raw text")
    log.info(f"    GET  /api/outputs        — List scripts")
    log.info(f"    GET  /api/health         — Health check")
    log.info("=" * 50)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Paper2Code")
    parser.add_argument("--pdf",       type=str,  help="Path to PDF (CLI mode)")
    parser.add_argument("--framework", type=str,  choices=["pytorch", "tensorflow"])
    parser.add_argument("--server",    action="store_true", help="Start Flask server")
    args = parser.parse_args()

    if args.server:
        run_server()
    elif args.pdf:
        run_cli(args.pdf, framework=args.framework)
    else:
        print("Usage:")
        print("  python main.py --server")
        print("  python main.py --pdf paper.pdf --framework pytorch")
        parser.print_help()
