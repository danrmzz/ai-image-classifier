import os
from flask import Flask, render_template, request

app = Flask(__name__)

# set the folder where uploaded files will be saved
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# make sure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

    # for now, return a success message with the file name
    return f"File successfully uploaded {file.filename}"

if __name__ == "__main__":
    app.run(debug=True)