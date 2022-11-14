import streamlit as st
import pickle
import numpy as np

def criaDummies(array):
    if array[2]== 0:        
        newArr = array[:2] + array[3:] + [1,0,0,0]
    elif array[2]== 1:        
        newArr = array[:2] + array[3:] + [0,1,0,0]
    elif array[2]== 2:        
        newArr = array[:2] + array[3:] + [0,0,1,0]                            
    else:        
        newArr = array[:2] + array[3:] + [0,0,0,1]                        
    return newArr

def load_model():
    with open('saved_data.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

modelo = data["model"]
transdict = data["dict"]

def show_predict_page():
    st.title("Heart Attack Prediction")

    st.write("""### Please enter the following details:""")

    rest_ecg = (
        "Normal",
        "Having ST-T",
        "Hypertrophy",
    )

    cp = (
        "Typical Angina",
        "Atypical Angina",
        "Non-anginal Pain",
        "Asymptomatic",
    )

    sex = (
        "Man",
        "Woman",
    )

    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    sex = st.selectbox("Sex",sex)
    exang = st.selectbox("Exercise Induced Angina",("Yes","No"))
    ca = st.number_input("Number of major vessels", min_value=0, max_value=3, value=0)
    cp = st.selectbox("Chest Pain Type",cp)
    trtbps = st.number_input("Resting Blood Pressure", min_value=94, max_value=200, value=120)
    chol =  st.slider("Cholestoral in mg/dl", min_value=0., max_value=10., value=3.)
    fbs = st.radio("Fasting Blood Sugar > 120 mg/dl",("True","False"))
    restEcg = st.selectbox("Resting Electrocardiographic Results", rest_ecg)
    thalach = st.slider("Maximum Heart Rate Achieved", min_value=70, max_value=200, value=100)

    # file = st.file_uploader("Upload a file")

    button = st.button("Predict")
    if button:
        X = [age,sex,cp,trtbps,chol,fbs,restEcg,thalach,exang,ca]
        X = [transdict.get(i, i) for i in X]
        X = criaDummies(X)
        X = np.asarray(X)
        X = X.reshape(1,-1)

        prediction = modelo.predict(X)
        if (prediction[0] == 0):
            st.subheader(prediction)
            st.subheader("The Person does not have a Heart Disease")
        else:
            st.subheader(prediction)
            st.subheader("The Person has Heart Disease")
    

