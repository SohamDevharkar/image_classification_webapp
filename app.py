from flask import Flask , render_template , request
from werkzeug.utils import secure_filename 
from db import db_init ,db
from dbmodel import ImagePredictionLog1
from keras.preprocessing.image import load_img, img_to_array

from keras.models import load_model
import numpy as np
import os



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
app.config["SQLALCHEMY_TRACE_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = "\pics"
db_init(app)

ALLOWED_EXTENSIONS = ['jpg','png','jpeg']

ai_model = load_model("models/mnist-comet.h5")

@app.route('/upload', methods = ['POST'])
def upload():
    try:
        if request.method == 'POST':
        
            image_file = request.files["image"]
        
            if allowed_file(image_file.filename):
                file_name = secure_filename(image_file.filename)
                mimetype = image_file.mimetype
                image_file.save(os.path.join('pics',file_name))
                
                
            imagepath = f'pics/{file_name}'
            #print(imagepath)
            preprocessed_image = preprocess_image(imagepath)
                 
                 
            prediction = ai_model.predict(preprocessed_image)
        
            predicted_class = np.argmax(prediction[0])
            
            
            print(predicted_class)
        
            log_entry = ImagePredictionLog1( 
                                       image_mimeType =mimetype,
                                       image_path = imagepath,
                                       image_name = file_name, 
                                       prediction_result = str(predicted_class)
                                       )
            
            
            db.session.add(log_entry)
            db.session.commit()
       
        
        return render_template("result.html",prediction = str(predicted_class))  
        
        #return jsonify({"message":"DONE"})
    except Exception as e:
        print(e)
        return render_template('result.html',error =str(e))

    
@app.route('/')
def main():
    return render_template('index.html')


def preprocess_image(img_path):
    # loading image with the required size
    i = load_img(img_path, target_size=(28,28))
    # normalize the pixel values from 0 to 1
    i = img_to_array(i)/255.0
    # reshaping the image array to fit the input layer of model.
    i = i.reshape(-1,784)
    return i

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True)
