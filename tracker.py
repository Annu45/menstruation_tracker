# ...existing code...
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

class PeriodTracker:
    def __init__(self, data_file="period_data.csv"):
       
        base_dir = os.path.dirname(__file__)
        self.data_file = os.path.abspath(os.path.join(base_dir, data_file))
        self.load_data()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_file, parse_dates=["start_date", "end_date"])
        except Exception:
           
            self.df = pd.DataFrame(columns=["start_date", "end_date", "flow", "symptoms"])
            self.save()
            return

       
        self.df["start_date"] = pd.to_datetime(self.df["start_date"], errors="coerce")
        self.df["end_date"] = pd.to_datetime(self.df["end_date"], errors="coerce")
        self.df = self.df.dropna(subset=["start_date", "end_date"]).copy()
        self.df = self.df.sort_values("start_date").reset_index(drop=True)
        
        self.save()

    def save(self):
        dirpath = os.path.dirname(self.data_file)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        self.df.to_csv(self.data_file, index=False)

    def add_period(self, start, end, flow="Medium", symptoms=""):
        start_date = pd.to_datetime(start, errors="coerce")
        end_date = pd.to_datetime(end, errors="coerce")

        if pd.isna(start_date) or pd.isna(end_date):
            return "⚠️ Invalid date format. Use YYYY-MM-DD."

        if end_date < start_date:
            return "⚠️ End date cannot be before start date."

       
        if not self.df[self.df["start_date"] == start_date].empty:
            dup_msg = "⚠️ An entry with this start date already exists; added as new record."
        else:
            dup_msg = ""

        new_entry = pd.DataFrame({
            "start_date": [start_date],
            "end_date": [end_date],
            "flow": [flow],
            "symptoms": [symptoms],
        })

        self.df = pd.concat([self.df, new_entry], ignore_index=True)
        self.df = self.df.sort_values("start_date").reset_index(drop=True)
        self.save()
        return ("✅ Period added successfully! " + dup_msg).strip()

    def _clean_df(self):
        dfc = self.df.dropna(subset=["start_date", "end_date"]).copy()
        dfc = dfc.sort_values("start_date").reset_index(drop=True)
        return dfc

    def calculate_stats(self):
        dfc = self._clean_df()
        if len(dfc) < 2:
            return {"message": "⚠️ Add at least 2 valid records for statistics."}

        cycles = dfc["start_date"].diff().dt.days.iloc[1:].dropna().astype(int)
        durations = ((dfc["end_date"] - dfc["start_date"]).dt.days + 1).dropna().astype(int)

        if cycles.empty or durations.empty:
            return {"message": "⚠️ Insufficient valid data to compute statistics."}

        stats = {
            "total_periods": int(len(dfc)),
            "average_cycle": round(float(cycles.mean()), 1),
            "cycle_range": f"{int(cycles.min())} – {int(cycles.max())} days",
            "average_duration": round(float(durations.mean()), 1),
        }
        return stats

    def predict_next_period(self):
        dfc = self._clean_df()
        if len(dfc) < 2:
            return {"message": "⚠️ Add at least 2 records for prediction."}

        cycles = dfc["start_date"].diff().dt.days.iloc[1:].dropna().astype(int)
        if cycles.empty:
            return {"message": "⚠️ Unable to compute cycle length for prediction."}

        avg_cycle = round(float(cycles.mean()), 1)
        days_to_add = int(round(avg_cycle))
        last_start = dfc["start_date"].iloc[-1]
        next_date = last_start + timedelta(days=days_to_add)

        return {
            "predicted_next_date": next_date.strftime("%Y-%m-%d"),
            "average_cycle_days": avg_cycle,
            "based_on_records": int(len(dfc))
        }

    def visualize_data(self):
        dfc = self._clean_df()
        if dfc.empty:
            return None

        durations = ((dfc["end_date"] - dfc["start_date"]).dt.days + 1).astype(int)
        labels = dfc["start_date"].dt.strftime("%Y-%m-%d")

        symptoms = {}
        for s in dfc["symptoms"].dropna().astype(str):
            for sym in s.split(","):
                sym = sym.strip().capitalize()
                if sym:
                    symptoms[sym] = symptoms.get(sym, 0) + 1

        fig, axs = plt.subplots(1, 2, figsize=(12, 6))
        fig.suptitle("🌸 Menstrual Health Insights 🌸", fontsize=18, color="#FF1493")

        axs[0].bar(labels, durations, color="#FF69B4", edgecolor="black")
        axs[0].set_title("Cycle Duration (Days)")
        axs[0].set_xlabel("Start Date")
        axs[0].set_ylabel("Duration (days)")
        axs[0].tick_params(axis="x", rotation=45)

        if symptoms:
            colors = ["#FFB6C1", "#FF69B4", "#FF91A4", "#FFC0CB", "#FFD1DC"]
            axs[1].pie(
                list(symptoms.values()),
                labels=list(symptoms.keys()),
                autopct='%1.1f%%',
                startangle=90,
                colors=colors[:len(symptoms)]
            )
            axs[1].set_title("Symptom Distribution")
        else:
            axs[1].text(0.5, 0.5, "No symptoms recorded", ha="center", va="center")
            axs[1].set_title("Symptom Distribution")
            axs[1].axis("off")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        # Save chart to an absolute path inside package folder
        chart_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "chart.png"))
        fig.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close(fig)

        return 
    

#     2025-04-27,2025-05-01,Medium,"cramps, fatigue"
# 2025-05-26,2025-05-30,Heavy,"backpain, bloating"