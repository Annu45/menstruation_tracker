# 🌸 Menstrual Health Tracker

A FastAPI + Gradio powered menstrual cycle tracking application that helps users log periods, analyze statistics, predict next cycles, and visualize health insights with beautiful charts.

---

## 🚀 Features

✔ **Track Your Periods**
- Add start and end dates
- Record flow intensity (Light/Medium/Heavy)
- Save symptoms (comma separated)

✔ **Cycle Statistics**
- Average cycle length
- Cycle range (min–max)
- Total recorded periods
- Average period duration

✔ **Smart Prediction**
- Predict the next expected start date
- Based on calculated average cycle length

✔ **Visual Insights**
- Bar chart: Cycle duration
- Pie chart: Symptom distribution
- Automatically generated chart image

✔ **Frontend + Backend Integration**
- Backend: FastAPI
- UI: Gradio (custom CSS + theme)
- Static file serving for charts & background images

---

## 🧩 Project Structure
menstruation_tracker/
│── static/
│    ├── chart.png
│    ├── image.png
│    ├── init.py
│    ├── app.py
│── tracker.py
│── period_data.csv
│── requirements.txt
---

## 🛠 Tech Stack
- Python 3
- FastAPI
- Gradio
- Pandas
- Matplotlib
- Uvicorn

---
