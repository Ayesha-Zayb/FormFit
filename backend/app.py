from flask import Flask, send_from_directory, jsonify
import subprocess
import sys
import os


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

BACKEND_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)

AI_DIR = os.path.join(
    BACKEND_DIR,
    "ai"
)

ANALYZER_PATH = os.path.join(
    AI_DIR,
    "pose_analyzer.py"
)


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# =========================================================
# FRONTEND FILES
# =========================================================

@app.route("/<path:filename>")
def frontend_files(filename):

    file_path = os.path.join(
        FRONTEND_DIR,
        filename
    )

    if os.path.isfile(file_path):

        return send_from_directory(
            FRONTEND_DIR,
            filename
        )

    return jsonify({
        "error": "File not found"
    }), 404


# =========================================================
# START EXERCISE ANALYSIS
# =========================================================

@app.route("/start-analysis")
def start_analysis():

    print("\n" + "=" * 60)
    print("FORMFIT: START ANALYSIS REQUEST RECEIVED")
    print("=" * 60)

    print(
        f"Analyzer: {ANALYZER_PATH}"
    )


    # -----------------------------------------------------
    # CHECK ANALYZER
    # -----------------------------------------------------

    if not os.path.isfile(ANALYZER_PATH):

        print(
            "ERROR: pose_analyzer.py was not found."
        )

        return jsonify({
            "success": False,
            "message": "Pose analyzer could not be found."
        }), 404


    # -----------------------------------------------------
    # PREPARE ENVIRONMENT
    # -----------------------------------------------------

    environment = os.environ.copy()

    existing_python_path = environment.get(
        "PYTHONPATH",
        ""
    )

    python_paths = [
        BASE_DIR,
        BACKEND_DIR
    ]

    if existing_python_path:

        python_paths.append(
            existing_python_path
        )

    environment["PYTHONPATH"] = os.pathsep.join(
        python_paths
    )


    # -----------------------------------------------------
    # START AI ANALYZER
    # -----------------------------------------------------

    try:

        print(
            "Starting FormFit AI analyzer..."
        )

        print(
            f"Python: {sys.executable}"
        )

        print(
            f"Working directory: {BACKEND_DIR}"
        )


        # Open the analyzer in a separate command window.
        #
        # /k keeps the window open if the analyzer
        # produces an error, allowing us to see it.

        subprocess.Popen(
            [
                "cmd",
                "/k",
                sys.executable,
                ANALYZER_PATH
            ],
            cwd=BACKEND_DIR,
            env=environment
        )


        print(
            "AI analyzer launch command sent successfully."
        )

        print("=" * 60 + "\n")


        return jsonify({
            "success": True,
            "message": "FormFit exercise analysis started."
        })


    except Exception as error:

        print(
            "\nFORMFIT AI START ERROR:"
        )

        print(
            str(error)
        )


        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "application": "FormFit",
        "service": "AI Fitness Analysis"
    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("FORMFIT AI FITNESS ANALYSIS")
    print("=" * 60)

    print(
        "Server: http://127.0.0.1:5000"
    )

    print(
        "Start Analysis: "
        "http://127.0.0.1:5000/start-analysis"
    )

    print(
        f"Analyzer: {ANALYZER_PATH}"
    )

    print("=" * 60)


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )