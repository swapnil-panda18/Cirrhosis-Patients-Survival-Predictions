from flask import Flask, render_template, request,jsonify
import joblib

#  Load pickle model


model = joblib.load(r'C:\Users\Dell\Desktop\Cirrhosis\Model\model.pkl')


app = Flask(__name__)

scaler = joblib.load(r'C:\Users\Dell\Desktop\Cirrhosis\Model\scaler.bin')



@app.route("/")
def home():
    return render_template('Index.html')

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        drug_selected = request.form['drug']
        drug = -1.0
        if drug_selected == "D-penicillamine":
            drug = 0.0
        elif drug_selected == "Placebo":
            drug = 1.0
        age = float(request.form['age'])  # range: (26.0,78.0)
        gender = request.form['sex']
        sex = -1.0
        if gender == 'Female':
            sex = 0.0
        elif gender == 'Male':
            sex = 1.0
        ascites_selected = request.form['ascites']
        ascites = -1.0
        if ascites_selected == 'No':
            ascites = 0.0
        elif ascites_selected == 'Yes':
            ascites = 1.0
        hepa_selected = request.form['hepatomegaly']
        hepatomegaly = -1.0
        if hepa_selected == 'No':
            hepatomegaly = 0.0
        elif hepa_selected == 'Yes':
            hepatomegaly = 1.0
        spider_selected = request.form['spiders']
        spider = -1.0
        if spider_selected == 'No':
            spider = 0.0
        elif spider_selected == 'Yes':
            spider = 1.0
        edema_selected = request.form['edema']
        edema = -1.0
        if edema_selected == 'No edema and no diuretic therapy for edema':
            edema = 0.0
        elif edema_selected == 'Edema present without diuretics, or edema resolved by diuretics':
            edema = 1.0
        elif edema_selected == 'Edema despite diuretic therapy':
            edema = 2.0
        bilirubin = float(request.form['bilirubin'])  
        cholesterol = float(request.form['cholesterol'])
        albumin = float(request.form['albumin'])
        copper = float(request.form['copper'])
        alk_phos = float(request.form['alk_phos'])
        sgot = float(request.form['sgot'])
        tryglycerides = float(request.form['tryglycerides'])
        platelets = float(request.form['platelets'])
        prothrombin = float(request.form['prothrombin'])
        stage = float(request.form['stage'])
        x_test = scaler.transform([[
            drug,
            age,
            sex,
            ascites,
            hepatomegaly,
            spider,
            edema,
            bilirubin,
            cholesterol,
            albumin,
            copper,
            alk_phos,
            sgot,
            tryglycerides,
            platelets,
            prothrombin,
        ]])
        #         print(X_test)
        predictions = model.predict(x_test)
        output = predictions[0]
        #         print(output)
        if output == 0:
            return render_template('home.html', prediction_text="The person with the given details has survival status c(censored).")
        elif output == 1:
            return render_template('home.html', prediction_text="The person with the given details has  survival status cl(censoreddue to liver transplantation).")
        elif output == 2:
            return render_template('home.html', prediction_text="The person with the given details has survival status D(death).")

# In[ ]:


if __name__ == "__main__":
    app.run(port=8080)