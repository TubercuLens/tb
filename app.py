from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from PIL import Image
import tensorflow as tf
import io


app = Flask(__name__)

# Load the pre-trained MobileNetV2 model
model = tf.keras.models.load_model('xray_model.h5')

def load_and_preprocess_image(file):
    img = Image.open(io.BytesIO(file.read()))
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    try:
        img = load_and_preprocess_image(file)
        prediction = model.predict(img)

        if prediction[0][0] > 0.5:
            return redirect(url_for('home'))
        else:
            return render_template('index.html', error='The provided image is not an X-ray.')
    except Exception as e:
        return render_template('index.html', error=f'Error processing the image: {str(e)}')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
