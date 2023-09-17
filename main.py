# pip3 install flask opencv-python
# python interpreter should be same as the virual env otherwise Flask won't be imported.
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import os
import cv2 #importing OpenCV

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}") # reading image into uploads
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_filename = f"static/{filename}"
            cv2.imwrite(f"static/{filename}", imgProcessed)
            return new_filename
        case "cwebp":
            new_filename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(new_filename, img) 
            return new_filename
        case "cjpg":
            new_filename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(new_filename, img) 
            return new_filename
        case "cpng":
            new_filename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(new_filename, img) 
            return new_filename
    pass


# endpoints :
@app.route("/") 
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template() 
  
@app.route("/edit", methods=["GET","POST"]) 
def edit():
    if request.method == "POST":  
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "Error: no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been successfully edited and is available <a href='/{new}'> here </a>")        
            return render_template("index.html")
        
    return render_template("index.html")

app.run(debug=True, port=5001) #to run the server
# i used 5001 port as on mac 5000 is busy sometimes 
