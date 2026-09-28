
from flask import Flask, render_template, jsonify
from flask_cors import CORS

from config import Config
from database.db import init_db

from routes.exam_routes import exam_bp
from routes.upload_routes import upload_bp
from routes.evaluation_routes import evaluation_bp
from routes.result_routes import result_bp


def create_app():
    """
    Flask Application Factory
    """

    # ---------------------------------------------------------
    # Create Flask application
    # ---------------------------------------------------------
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # ---------------------------------------------------------
    # Load configuration
    # ---------------------------------------------------------
    app.config.from_object(Config)

    # ---------------------------------------------------------
    # Enable CORS
    # ---------------------------------------------------------
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*"
            }
        }
    )

    # ---------------------------------------------------------
    # Initialize Database
    # ---------------------------------------------------------
    try:
        init_db()
        app.logger.info("Database initialized successfully.")
    except Exception as e:
        app.logger.error(
            f"Database initialization failed: {str(e)}"
        )

    # ---------------------------------------------------------
    # Register API Blueprints
    # ---------------------------------------------------------

    app.register_blueprint(
        exam_bp,
        url_prefix="/api/exam"
    )

    app.register_blueprint(
        upload_bp,
        url_prefix="/api/upload"
    )

    app.register_blueprint(
        evaluation_bp,
        url_prefix="/api/evaluation"
    )

    app.register_blueprint(
        result_bp,
        url_prefix="/api/result"
    )

    # =========================================================
    # FRONTEND ROUTES
    # =========================================================

    # ---------------------------------------------------------
    # Home Page
    # ---------------------------------------------------------
    @app.route("/")
    def home():
        return render_template("index.html")

    # ---------------------------------------------------------
    # Dashboard Page
    # ---------------------------------------------------------
    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    # ---------------------------------------------------------
    # Upload Page
    # ---------------------------------------------------------
    @app.route("/upload")
    def upload_page():
        return render_template("upload.html")

    # ---------------------------------------------------------
    # Evaluation Page
    # ---------------------------------------------------------
    @app.route("/evaluation")
    def evaluation_page():
        return render_template("evaluation.html")

    # ---------------------------------------------------------
    # Results Page
    # ---------------------------------------------------------
    @app.route("/results/<student_id>")
    def results_page(student_id):
        return render_template(
            "results.html",
            student_id=student_id
        )

    # =========================================================
    # SYSTEM / API ROUTES
    # =========================================================

    # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "running",
            "project": "AI-Driven Examination & OSM",
            "version": "1.0.0"
        }), 200

    # ---------------------------------------------------------
    # API Information
    # ---------------------------------------------------------
    @app.route("/api", methods=["GET"])
    def api_info():
        return jsonify({
            "status": "success",
            "message": "AI-Driven Examination & On-Screen Marking API",
            "version": "1.0.0",
            "endpoints": {
                "exam": "/api/exam",
                "upload": "/api/upload",
                "evaluation": "/api/evaluation",
                "result": "/api/result",
                "health": "/health"
            }
        }), 200

    # ---------------------------------------------------------
    # 404 Error Handler
    # ---------------------------------------------------------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "The requested resource was not found."
        }), 404

    # ---------------------------------------------------------
    # 500 Error Handler
    # ---------------------------------------------------------
    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.exception(
            "Internal server error occurred."
        )

        return jsonify({
            "status": "error",
            "message": "Internal server error."
        }), 500

    # ---------------------------------------------------------
    # Global Exception Handler
    # ---------------------------------------------------------
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.exception(
            "Unhandled application exception."
        )

        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred."
        }), 500

    return app


# =============================================================
# CREATE APPLICATION
# =============================================================

app = create_app()


# =============================================================
# RUN APPLICATION
# =============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

