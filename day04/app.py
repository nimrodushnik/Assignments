
from flask import Flask, render_template, request
import scipy.io as sio
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import re
import io
import base64

app = Flask(__name__)


def create_plot(file):
    data = sio.loadmat(file.stream, simplify_cells=True)
    fs = 1000

    # Find and sort trials
    trial_names = sorted(
        [name for name in data if re.fullmatch(r"Trial\d+", name)],
        key=lambda name: int(name[5:])
    )

    # Plot licks
    plt.figure()

    for i, name in enumerate(trial_names, start=1):
        licks = np.ravel(data[name]["AnalogData"]["Button"]["Btn1"])

        lick_idx = np.where(np.diff(np.r_[0, licks]) == 1)[0]
        lick_times = lick_idx / fs

        plt.plot(lick_times, [i] * len(lick_times), "k.", markersize=4)

    # Odor markers
    plt.axvline(0, color="red", linestyle="--", label="Odor Start")
    plt.axvline(2, color="red", linestyle="--", label="Odor End")

    plt.xlim(-0.01, 7)
    plt.ylim(len(trial_names), 1)
    plt.yticks([1, 50, 100, 150, 200])
    plt.xlabel("Time (s)")
    plt.ylabel("Trial #")
    plt.title("Lick Raster Plot")
    plt.grid(True)
    plt.legend()

    # Convert plot into an image
    image = io.BytesIO()
    plt.savefig(image, format="png", bbox_inches="tight")
    plt.close()

    image.seek(0)
    return base64.b64encode(image.getvalue()).decode("utf-8")


@app.route("/", methods=["GET", "POST"])
def home():
    plot = None
    error = None

    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename.lower().endswith(".mat"):
            try:
                plot = create_plot(file)
            except Exception as e:
                error = str(e)
                print("ERROR:", e)
        else:
            error = "Please upload a .mat file."

    return render_template("index.html", plot=plot, error=error)


if __name__ == "__main__":
    app.run(debug=True)
