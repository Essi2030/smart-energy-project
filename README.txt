# 🏢 Smart Energy Monitoring Dashboard with AI & IoT

A real-time, AI-powered dashboard for predicting and monitoring electricity consumption in smart buildings — designed for deployment in the UAE Smart City ecosystem.

---

## 🔥 Why this project matters

🏙️ The UAE is investing heavily in sustainable energy and smart buildings.  
This project aligns with UAE Vision 2031 by offering a real-time dashboard that combines:

- 📡 IoT sensor data (temperature, humidity, occupancy)
- 🧠 Machine Learning (XGBoost for energy forecasting)
- ⚙️ FastAPI (for scalable inference)
- 📊 Streamlit dashboard (with bilingual UI: English & Arabic)
- ☁️ Deployed on AWS EC2 with Nginx + HTTPS

---

## 🚀 Tech Stack

| Layer       | Tech                       |
|-------------|----------------------------|
| Frontend    | Streamlit (bilingual)      |
| Backend     | FastAPI                    |
| ML Model    | XGBoost + pandas           |
| Data        | Simulated IoT (sensor)     |
| Hosting     | AWS EC2 (Ubuntu 22.04)     |
| HTTPS       | Nginx + Certbot SSL        |
| Monitoring  | systemd + journalctl logs  |

---

## 📷 Screenshots

<img src="screenshots/form.png" width="400" />
<img src="screenshots/prediction_chart.png" width="400" />

---

## 🌍 Live Demo

🔗 https://dashboard.yourdomain.com (Live on AWS)

Username: `demo`  
Password: `smartai2025` (if auth enabled)

---

## 📦 Project Structure

smart-energy-project/
├── dashboard/ # Streamlit frontend
├── api/ # FastAPI backend
├── model/ # ML training scripts
├── utils/ # Data simulation
├── data/ # Sensor CSVs
├── requirements.txt
└── README.md


---

## 🧠 Future Enhancements

- Connect to real-time IoT sensors (MQTT or AWS IoT Core)
- Add user login (JWT-based)
- Migrate database to AWS RDS (PostgreSQL)
- Deploy via CI/CD pipeline (GitHub Actions)

---

## 🤝 Let's Connect

Feel free to explore, fork, and message me:

🔗 LinkedIn: [linkedin.com/in/dr-ehsan-zafari-ai-ml/](https://www.linkedin.com/in/dr-ehsan-zafari-ai-ml/)  
📧 Email: zafari.ehsan109@gmail.com  
🌍 GitHub: [github.com/Essi2030](https://github.com/Essi2030)

---
