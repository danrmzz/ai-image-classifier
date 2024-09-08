import os
from flask import Flask, render_template, request
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions # type: ignore
from tensorflow.keras.preprocessing.image import load_img, img_to_array # type: ignore



app = Flask(__name__)

# set the folder where uploaded files will be saved
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# make sure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# load the MobileNetV2 model (pre-trained on ImageNet)
model = MobileNetV2(weights="imagenet")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # check if the post request has the file part (checks if a file was submitted)
    if "file" not in request.files:
        return "No file part in the request"
    
    file = request.files["file"]

    # if the user doesn't select a file
    if file.filename == "":
        return "No file selected"
    
    # save the file in the upload folder
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # load the image and process it
    image = load_img(file_path, target_size=(224, 224)) # resize the image to 224x224
    image = img_to_array(image) # convert image to a numpy array so it an be passed to the model
    image = preprocess_input(image) # prepares the image in a format the model understands
    image = image.reshape((1, 224, 224, 3)) # reshape for the model (batch size of 1 required by the model)

    # make a prediction using the model
    predictions = model.predict(image)
    label = decode_predictions(predictions) # decode the results into human-readable labels
    label = label[0][0] # get the top result

    # display the result
    result = f"Prediction: {label[1]} with a confidence of {label[2]*100:.2f}%"

    return render_template("predict.html", filename=file.filename, label=label[1], confidence=round(label[2]*100, 2))

if __name__ == "__main__":
    app.run(debug=True)