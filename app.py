from fastapi import FastAPI
from pydantic import BaseModel #ensure sahi date format
from datetime import date
import gradio as gr   
import os
from fastapi.staticfiles import StaticFiles
from menstruation_tracker.tracker import PeriodTracker
from shutil import copyfile #chart image ko copy karne ke liye static folder me 

app = FastAPI(title="🌸 Menstrual Health Tracker API 🌸")
tracker = PeriodTracker()

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

# ------------ Pydantic Model ------------
class PeriodData(BaseModel):
    start_date: date
    end_date: date
    flow: str = "Medium"
    symptoms: str = ""

# ------------ FastAPI Endpoints ------------
@app.post("/add_period")
def add_period(data: PeriodData):
    msg = tracker.add_period(str(data.start_date), str(data.end_date), data.flow, data.symptoms)
    return {"message": msg}

@app.get("/stats")
def stats():
    return tracker.calculate_stats()

@app.get("/predict")
def predict():
    return tracker.predict_next_period()

@app.get("/visualize")
def visualize():
    img_path = tracker.visualize_data()
    static_img_path = os.path.join(STATIC_DIR, "chart.png")

    if img_path and os.path.exists(img_path):
        copyfile(img_path, static_img_path)
      
        return {"chart_path": "/static/chart.png"}

    return {"chart_path": None}


# ------------ Gradio Functions ------------
def gradio_add(start_date, end_date, flow, symptoms):
    return tracker.add_period(start_date, end_date, flow, symptoms)

def gradio_stats():
    return tracker.calculate_stats()

def gradio_predict():
    return tracker.predict_next_period()

def gradio_chart():
    img_path = tracker.visualize_data()
    static_img_path = os.path.join(STATIC_DIR, "chart.png")

    if img_path and os.path.exists(img_path):
        copyfile(img_path, static_img_path)
        
        return os.path.abspath(static_img_path)

    return None


# ------------ CSS (Background Image ) ------------
custom_css = """
html, body {
    background-image: url('/static/image.png');
    background-repeat: no-repeat;
    background-size: cover;
    
    background-attachment: fixed;
    height: 100%;
    margin: 0;
    padding: 0;
    font-family: 'Poppins', sans-serif;
}

.gradio-container {
    background: rgba(255, 240, 245, 0.80);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 25px rgba(255, 105, 180, 0.4);
}

#title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    color: #ff1493;
    margin-bottom: 0.3rem;
}

#subtitle {
    text-align: center;
    color: #7a0066;
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
}
"""


# ------------ Gradio UI Layout ------------
with gr.Blocks(css=custom_css, theme=gr.themes.Soft(primary_hue="pink")) as demo:

    gr.HTML("""
        <div id="title">🌸 Menstrual Health Tracker 🌸</div>
        <div id="subtitle">Track your periods, predict your next cycle, and visualize your health trends beautifully.</div>
    """)


    with gr.Tab("➕ Add Period Entry"):
        start = gr.Textbox(label="Start Date (YYYY-MM-DD)")
        end = gr.Textbox(label="End Date (YYYY-MM-DD)")
        flow = gr.Dropdown(["Light", "Medium", "Heavy"], value="Medium", label="Flow Intensity")
        symptoms = gr.Textbox(label="Symptoms (comma separated)")
        output = gr.Textbox(label="Status")
        gr.Button("Add Entry", variant="primary").click(
            gradio_add, 
            inputs=[start, end, flow, symptoms], 
            outputs=output
        )

    with gr.Tab("📊 Statistics"):
        gr.Button("Show Stats", variant="primary").click(gradio_stats, outputs=gr.JSON())

    with gr.Tab("🔮 Predict Next Period"):
        gr.Button("Predict", variant="primary").click(gradio_predict, outputs=gr.JSON())

    with gr.Tab("📈 Visualization"):
        gr.Button("Show Chart", variant="primary").click(gradio_chart, outputs=gr.Image(type="filepath"))

app = gr.mount_gradio_app(app, demo, path="/ui")