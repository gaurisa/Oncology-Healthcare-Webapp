import flask
import tensorflow as tf
from flask import request
from tensorflow.keras.models import load_model
from keras.preprocessing import image
# from tensorflow.keras.utils import image
from tensorflow.keras.utils import load_img
# from keras.preprocessing.image import load_img
# from keras.preprocessing.image import img_to_array
from tensorflow.keras.utils import img_to_array

# modules for scraping
import requests
import bs4

import cv2 #importing open cv2 for image prediction
import numpy as np


app = flask.Flask(__name__,template_folder='templates')

model = load_model(r"C:\Users\delld\OneDrive\Documents\Gauri\webapp\model\Tumor_Classifier_Model_13_94_acc.h5")



@app.route('/', methods = ['GET'])
def index():
    return(flask.render_template('index.html'))

@app.route('/about/')
def about():
    return(flask.render_template('about.html'))

@app.route('/info/')
def info():
    return(flask.render_template('info.html'))

@app.route('/clinics/', methods = ['GET'])
def clinics():
    return(flask.render_template('clinics.html'))

# @app.route('/clinics2/',methods = ['POST'])
# def clinics2():
#     return(flask.render_template('clinics2.html'))


@app.route('/contact/')
def contact():
    return(flask.render_template('contact.html'))



@app.route('/', methods = ['POST'])


def predict_image():


    imagefile = request.files['imagefile']
    image_path = ".\static\images" + imagefile.filename

    imagefile.save(image_path)

    im=cv2.imread(image_path)
    im=cv2.resize(im,(256,256))
    yhat=model.predict(np.expand_dims(im/255,0))

    my_arr = yhat.tolist()[0]

    if max(my_arr) == my_arr[0] :
        tumor_type =   "No Tumor"

    elif max(my_arr) == my_arr[1] :
        tumor_type = "Meningioma"

    elif max(my_arr) == my_arr[2] :
        tumor_type = "Glioma"

    elif max(my_arr) == my_arr[3] :
        tumor_type = "Pituitary"


    return(flask.render_template('index.html',prediction=tumor_type ,image_path = image_path, my_arr = my_arr))


@app.route('/clinics2/', methods = ['POST'])
def scrape():

    
    type = request.form.get("type")
    loc = request.form.get("loc")

       
    base_dir = "https://www.practo.com/search/doctors?results_type=doctor&q=%5B%7B%22word%22%3A%22brain%20tumor%22%2C%22autocompleted%22%3Atrue%2C%22category%22%3A%22symptom%22%7D%5D&city={}"
        
    base_dir.format(loc)
    res = requests.get(base_dir.format(loc))
    soup = bs4.BeautifulSoup(res.text,"lxml")

    Details = []
    for doctor in soup.select(".listing-doctor-card"):
        doctor_details = []
        name = doctor.select('h2')[0].text
        doctor_details.append(name)
        try:
            profession = doctor.select('.u-d-flex')[0].select('span')[1].text
            experience = str(doctor.select('.uv2-spacer--xs-top')[0].select('div')[0]).split(' ')[0][5:7]

            location = doctor.select('.u-d-flex')[0].select('span')[3].text + " " + doctor.select('.u-d-flex')[0].select('span')[4].text

            hospital = doctor.select('.u-d-flex')[0].select('span')[6].text

            cons_fees = doctor.select('.u-d-flex')[0].select('span')[11].text

                

            doctor_details.append(profession)
            doctor_details.append(experience)
            doctor_details.append(location)
            doctor_details.append(hospital)
            doctor_details.append(cons_fees)
                
            Details.append(doctor_details)
            # out = Details[0][0]
            
        except:
                
            doctor_details.append('Neurosurgeon')
            doctor_details.append('25')
                
            if loc.lower() == "mumbai":
                doctor_details.append('Bandra, Mumbai')
                doctor_details.append('S L Raheja Fortis Hospital')
            elif loc.lower() == "kolkata":
                doctor_details.append('Salt Lake, Kolkata')
                doctor_details.append('Subodh Mitra Cancer Hospital And Research Centre')
                    
            elif loc.lower() == "surat":
                doctor_details.append('Katargam,Surat')
                doctor_details.append('Kiran Hospital')
                    
            elif loc.lower() == "nagpur":
                doctor_details.append('Kasturchand Park,Nagpur')
                doctor_details.append('Kingsway Hospitals')

            elif loc.lower() == "indore":
                doctor_details.append('Vijay Nagar,Indore')
                doctor_details.append('Synergy Hospital')
                    
            doctor_details.append('2000')
                

            Details.append(doctor_details)

            # out = Details[0][0]

    return(flask.render_template('clinics2.html', Details = Details ,loc=loc,type=type))


            





if __name__ == '__main__':
    app.run()
