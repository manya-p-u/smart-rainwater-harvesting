from flask import Flask, render_template, request
import pandas as pd
import sqlite3
from calculator.rainwater_calculator import calculate_water

app = Flask(__name__)

# ===============================
# LOAD DATASET
# ===============================
data = pd.read_csv("data/rainfall_data.csv")
data = data.fillna(0)

# ===============================
# DATABASE
# ===============================
conn = sqlite3.connect("database.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS history(
    location TEXT,
    water REAL,
    rainfall REAL
)
""")
conn.commit()

# ===============================
# HOME
# ===============================
@app.route("/")
def home():
    locations = data["SUBDIVISION"].unique()
    return render_template("index.html", locations=locations)

# ===============================
# CALCULATOR
# ===============================
@app.route("/calculator", methods=["GET", "POST"])
def calculator():

    locations = data["SUBDIVISION"].unique()

    if request.method == "POST":

        roof_area = float(request.form["roof_area"])
        family = int(request.form["family"])
        location = request.form["location"]

        rainfall = data[data["SUBDIVISION"] == location]["ANNUAL"].mean()

        # ML prediction (simple)
        predicted = round(rainfall * 1.05, 2)

        water = calculate_water(roof_area, rainfall, 0.8)

        demand = family * 135 * 365
        coverage = round((water / demand) * 100, 2)

        savings = round(water * 0.05, 2)

        # Tank recommendation
        if water < 50000:
            tank = "2000 Liters"
        elif water < 150000:
            tank = "5000 Liters"
        else:
            tank = "10000 Liters"

        method = "Recharge Pit System" if rainfall > 2000 else "Storage Tank System"

        # Save to DB
        cur.execute("INSERT INTO history VALUES (?,?,?)",
                    (location, water, rainfall))
        conn.commit()

        message = f"You can meet approximately {coverage}% of your yearly water demand."

        return render_template(
            "result.html",
            location=location,
            rainfall=round(rainfall,2),
            predicted=predicted,
            water=round(water,2),
            demand=demand,
            coverage=coverage,
            savings=savings,
            tank=tank,
            method=method,
            message=message
        )

    return render_template("calculator.html", locations=locations)

# ===============================
# DASHBOARD
# ===============================
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():

    locations = data["SUBDIVISION"].unique()
    location = request.form.get("location", locations[0])

    row = data[data["SUBDIVISION"] == location].iloc[0]

    months = ["JAN","FEB","MAR","APR","MAY","JUN",
              "JUL","AUG","SEP","OCT","NOV","DEC"]

    rainfall_values = [row[m] for m in months]

    # ✅ Static weather (no API needed)
    temperature = 28  # You can change manually

    return render_template(
        "dashboard.html",
        rainfall=rainfall_values,
        location=location,
        locations=locations,
        temperature=temperature
    )

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(debug=True)