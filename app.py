import os
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.applications import MobileNetV2 # type: ignore
from tensorflow.keras.preprocessing.image import load_img, img_to_array # type: ignore
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions # type: ignore
import numpy as np

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load pre-trained MobileNetV2 model
model = MobileNetV2(weights="imagenet")

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if the post request has the file part
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            # Save the uploaded file
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            # Preprocess the image
            image = load_img(file_path, target_size=(224, 224))  # MobileNetV2 input size
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = preprocess_input(image)

            # Predict the class
            predictions = model.predict(image)
            decoded_predictions = decode_predictions(predictions, top=1)[0]
            predicted_class = decoded_predictions[0][1]  # Get class label

            return render_template(
                "index.html",
                prediction=predicted_class,
                image_path=file_path
            )
    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    app.run(debug=True)
