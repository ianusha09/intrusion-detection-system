# 🔐 Area-Restricted Intrusion Detection System

> A real-time AI-powered security system that monitors a restricted area through a live webcam feed and triggers alerts when an unauthorized person is detected inside the zone.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=flat-square&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

---

## 📌 Overview

Traditional security systems rely on manual monitoring, which is inefficient and prone to human error. This project replaces manual surveillance with an **automated, intelligent intrusion detection system** that:

- Continuously monitors a live camera feed
- Uses **AI-based human pose detection** (not simple motion detection)
- Defines a **restricted polygon zone** on the frame
- Fires an alert only when a person stays inside the zone for a set duration
- Sends an **SMS notification** via Twilio and logs all events

This was developed as a **Minor Project** for the B.Tech Computer Science program.

---

## 🎯 Features

| Feature | Details |
|---|---|
| 👁️ Live Monitoring | Real-time webcam feed processed frame by frame |
| 🤖 AI Pose Detection | MediaPipe detects 33 human body landmarks |
| 📐 Restricted Zone | Customizable polygon zone drawn on the video |
| 🎨 Visual Feedback | Zone turns red when intruder detected |
| ⏱️ Time-Based Alert | Alert fires only after 3 continuous seconds in zone |
| 📱 SMS Alert | Twilio sends instant SMS to configured number |
| 🔕 Cooldown System | 15-second cooldown prevents repeated alert spam |
| 📋 Event Logging | Every entry, exit, and alert logged to console |
| ❌ False Alarm Filter | Passing-by persons do not trigger alerts |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.10** | Core programming language |
| **OpenCV** | Video capture, frame processing, UI rendering |
| **cvzone 1.6.1** | Simplified MediaPipe Pose wrapper |
| **MediaPipe** | AI/ML pose estimation (33 body landmarks) |
| **NumPy** | Polygon zone definition and math |
| **Twilio** | Cloud SMS alert delivery |

---

## 🧠 How It Works

```
Start Camera
     ↓
Capture Frame → Flip (mirror)
     ↓
Run MediaPipe Pose Detection
     ↓
Human detected?
  ↓ NO                     ↓ YES
Reset timer         Extract nose landmark (x, y)
Repeat                      ↓
               Inside restricted polygon? (pointPolygonTest)
                 ↓ NO               ↓ YES
             Reset timer       Start / continue timer
             Repeat                  ↓
                            Timer ≥ 3 seconds?
                              ↓ NO       ↓ YES
                            Repeat   INTRUSION CONFIRMED
                                         ↓
                              Flash banner on screen
                              Log to console
                              Send SMS via Twilio
                              Start 15s cooldown
```

**Key Detection Logic:**
1. MediaPipe extracts the **nose landmark (x, y)** as the person's position
2. `cv2.pointPolygonTest()` checks if this point is inside the restricted polygon
3. A **3-second continuous timer** confirms genuine intrusion vs. passerby
4. Alert triggers → SMS sent → **15-second cooldown** begins

---

## 📁 Project Structure

```
Intrusion-detection-system/
│
├── main.py          # Core system — detection, zone logic, visual UI
├── send.py          # Alert module — Twilio SMS integration
├── requirements.txt # All dependencies
└── README.md        # This file
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Intrusion-detection-system.git
cd Intrusion-detection-system
```

### 2. Create Virtual Environment (Python 3.10 required)
```bash
py -3.10 -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure SMS Alerts (Optional)
Open `send.py` and fill in your Twilio credentials:
```python
ACCOUNT_SID = "your_twilio_account_sid"
AUTH_TOKEN  = "your_twilio_auth_token"
FROM_PHONE  = "+1xxxxxxxxxx"   # Your Twilio number
TO_PHONE    = "+91xxxxxxxxxx"  # Your personal number
```
> 💡 Skip this step if you only want visual alerts. The system works without Twilio — it just logs to console instead.

### 5. Run the System
```bash
python main.py
```

---

## 🖥️ Usage

- A window opens showing your live webcam feed
- A **yellow box** marks the restricted zone on screen
- Walk into the box — it turns **red** and starts the timer
- Stay inside for **3 seconds** → intrusion alert fires
- Press **Q** to quit

### Customizing the Restricted Zone
In `main.py`, edit the `RESTRICTED_ZONE` coordinates to reposition or resize the zone:
```python
RESTRICTED_ZONE = np.array([
    [150, 100],   # Top-left
    [500, 100],   # Top-right
    [500, 400],   # Bottom-right
    [150, 400]    # Bottom-left
], np.int32)
```

---

## 📦 Requirements

```
opencv-python
cvzone==1.6.1
mediapipe
twilio
numpy
```

> ⚠️ **Python 3.10 is required.** MediaPipe does not currently support Python 3.11+.

---

## 🚀 Future Enhancements

- [ ] Web dashboard (React + Flask) for remote monitoring
- [ ] Email alert support
- [ ] Multiple restricted zones
- [ ] Recording and saving intrusion clips
- [ ] Night vision / low-light support
- [ ] Mobile app integration

---

## 👨‍💻 Author

Anusha — B.Tech Computer Science (AI & ML)
Minor Project

---

## 📄 License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

---

## 🙏 Acknowledgements

- [cvzone by Computer Vision Zone](https://github.com/cvzone/cvzone)
- [MediaPipe by Google](https://mediapipe.dev)
- [OpenCV](https://opencv.org)
- [Twilio](https://twilio.com)
