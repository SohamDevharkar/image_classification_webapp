from db import db

class ImagePredictionLog1(db.Model):
    
    image_id = db.Column(db.Integer,primary_key = True)
    #img = db.Column(db.String(80),nullable=False)
    image_name = db.Column(db.Text(20),nullable=False)
    image_mimeType = db.Column(db.Text,nullable=False)
    image_path = db.Column(db.Text,nullable=False)
    prediction_result = db.Column(db.Text,nullable=False)
    
