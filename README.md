<div align="center">

<img src="formfit-banner.png" alt="FormFit Banner" width="100%">

# FormFit

### AI-Powered Exercise Form Analysis & Repetition Tracking

Computer vision and human pose estimation for real-time exercise movement analysis.

</div>

---

## About FormFit

**FormFit** is an AI-powered fitness application that uses computer vision and human pose estimation to analyze exercise movements in real time.

The application captures movement through a webcam, detects human body landmarks using **MediaPipe**, and analyzes body positioning and joint angles to support exercise repetition tracking and form analysis.

FormFit combines a **Python Flask backend, computer vision, pose estimation, movement analysis, and a browser-based frontend** into a modular fitness application.

The project was developed to demonstrate the practical use of artificial intelligence and computer vision in fitness technology.

---

## Key Features

* **Real-Time Pose Estimation** — Detects human body landmarks using MediaPipe.
* **Webcam-Based Analysis** — Processes live camera input for exercise analysis.
* **Movement Analysis** — Uses body landmarks and joint angles to evaluate movement.
* **Repetition Tracking** — Tracks exercise repetitions based on movement states.
* **Exercise Form Analysis** — Provides form-related analysis during supported exercises.
* **Range of Motion Analysis** — Uses joint positioning to evaluate movement range.
* **Performance Metrics** — Generates exercise-related measurements during analysis.
* **Interactive Web Interface** — Provides a browser-based interface for starting and monitoring analysis.
* **Modular Architecture** — Separates frontend, backend, and AI analysis components.

---

## How It Works

FormFit follows a computer-vision-based processing pipeline:

```text
Webcam Input
      │
      ▼
Frame Capture
      │
      ▼
Pose Detection
      │
      ▼
Body Landmark Extraction
      │
      ▼
Joint Angle Calculation
      │
      ▼
Movement Analysis
      │
      ▼
Repetition Tracking
      │
      ▼
Exercise Form Analysis
      │
      ▼
Performance Information
```

The webcam provides live frames to the AI analysis component. MediaPipe detects the user's body landmarks, after which relevant joint angles and movement patterns are analyzed.

The analysis is then used to identify exercise movement states, track repetitions, and generate exercise-related performance information.

---

## System Architecture

```text
                         ┌───────────────────┐
                         │       User        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │     Frontend      │
                         │ HTML / CSS / JS   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Flask Backend     │
                         │   app.py          │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   AI Analysis     │
                         │ Pose Estimation   │
                         └─────────┬─────────┘
                                   │
                         ┌─────────┴─────────┐
                         ▼                   ▼
                ┌────────────────┐  ┌────────────────┐
                │ MediaPipe Pose │  │ Angle Analysis │
                │   Landmarks    │  │ & Movement     │
                └────────────────┘  └────────────────┘
```

---

## Technology Stack

| Technology     | Purpose                                              |
| -------------- | ---------------------------------------------------- |
| **Python**     | Core application development                         |
| **Flask**      | Backend web application and API routes               |
| **OpenCV**     | Webcam access, frame processing, and computer vision |
| **MediaPipe**  | Human pose estimation and body landmark detection    |
| **NumPy**      | Numerical processing and data operations             |
| **HTML5**      | Frontend structure                                   |
| **CSS3**       | Frontend styling                                     |
| **JavaScript** | Frontend interaction and API communication           |

---

## Project Structure

```text
FormFit/
│
├── backend/
│   ├── app.py
│   │   └── Flask backend and application routes
│   │
│   └── ai/
│       ├── angle_calculator.py
│       │   └── Joint-angle calculations
│       │
│       ├── pose_analyzer.py
│       │   └── MediaPipe pose analysis and exercise tracking
│       │
│       └── pose_landmarker_full.task
│           └── MediaPipe pose landmark model
│
├── frontend/
│   ├── index.html
│   │   └── Main web interface
│   │
│   ├── script.js
│   │   └── Frontend interaction and backend communication
│   │
│   └── style.css
│       └── Interface styling
│
├── dashboard.py
│   └── Dashboard-related application component
│
├── .gitignore
│   └── Git exclusion rules
│
├── README.md
│   └── Project documentation
│
├── requirements.txt
│   └── Python dependencies
│
├── LICENSE
│   └── MIT License
│
└── formfit-banner.png
    └── Repository banner
```

> Virtual environments such as `venv/`, `venv_old/`, and `venv312/` are local development environments and are intentionally excluded from version control.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ayesha-Zayb/FormFit.git
```

### 2. Navigate to the Project

```bash
cd FormFit
```

### 3. Create a Virtual Environment

For Python 3.12:

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell**

```powershell
venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```cmd
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running FormFit

Start the Flask backend from the project root:

```bash
python backend/app.py
```

The application will start on:

```text
http://127.0.0.1:5000
```

Open the address in a web browser to access the FormFit interface.

### Health Check

FormFit also provides a health-check endpoint:

```text
http://127.0.0.1:5000/health
```

A successful response indicates that the backend service is online.

### Starting Exercise Analysis

The application exposes the analysis endpoint:

```text
http://127.0.0.1:5000/start-analysis
```

The frontend can use this endpoint to launch the AI exercise analysis process.

---

## Camera Requirements

FormFit uses a webcam for real-time exercise analysis.

For best results:

* Use a working webcam.
* Position the camera so the relevant body landmarks are visible.
* Maintain sufficient lighting.
* Stand far enough from the camera for the required body joints to remain visible.
* Perform supported exercises within the camera's field of view.

Because pose estimation depends on visible body landmarks, camera positioning and lighting can affect detection accuracy.

---

## AI Analysis

The AI component is built around **MediaPipe Pose Landmarker**.

The analysis pipeline uses detected body landmarks to calculate joint angles and interpret movement.

The project includes the required model asset:

```text
backend/ai/pose_landmarker_full.task
```

The main analysis component is:

```text
backend/ai/pose_analyzer.py
```

Joint-angle calculations are handled by:

```text
backend/ai/angle_calculator.py
```

Together, these components provide the foundation for exercise movement analysis and repetition tracking.

---

## Backend

The Flask backend is located at:

```text
backend/app.py
```

It provides:

* Frontend file serving
* Application routing
* Health monitoring
* Exercise-analysis initiation
* Communication between the web interface and the AI analysis component

The backend launches the AI analyzer as a separate process when exercise analysis is requested.

---

## Frontend

The browser interface is contained within the `frontend/` directory.

### HTML

```text
frontend/index.html
```

Defines the main application interface.

### CSS

```text
frontend/style.css
```

Provides the visual design and layout.

### JavaScript

```text
frontend/script.js
```

Handles frontend interaction and communication with the Flask backend.

---

## Project Preview

The repository includes a dedicated project banner at the top of this README.

Additional screenshots can be added in future updates to demonstrate:

* FormFit dashboard
* Exercise analysis interface
* Real-time pose detection
* Repetition tracking
* Performance information

---

## Development Focus

FormFit demonstrates practical applications of:

* Computer vision
* Human pose estimation
* Real-time webcam processing
* Body landmark detection
* Joint-angle calculation
* Movement analysis
* Exercise repetition tracking
* Exercise form analysis
* Flask backend development
* Frontend and backend integration
* AI-assisted fitness technology

---

## Future Improvements

Potential future versions of FormFit may include:

* Support for additional exercises
* More advanced form correction
* Improved repetition detection
* Personalized workout recommendations
* Workout history and progress tracking
* Expanded performance analytics
* User authentication and profiles
* More detailed exercise feedback
* Mobile application support
* Cloud-based synchronization
* Advanced AI-assisted fitness features

---

## License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for complete license information.

---

## Author

**Ayesha Zaib Warraich**

[GitHub](https://github.com/Ayesha-Zayb)

---

<div align="center">

**FormFit**

*Intelligent exercise analysis through computer vision and pose estimation.*

</div>
