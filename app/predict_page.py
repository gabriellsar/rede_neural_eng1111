import streamlit as st
import pickle
import numpy as np

def criaDummies(array):
    newArr = array[:2] + array[3:]
    if array[2]== 0:        
        newArr += [1,0,0,0]
    elif array[2]== 1:        
        newArr += [0,1,0,0]
    elif array[2]== 2:        
        newArr += [0,0,1,0]                            
    else:        
        newArr += [0,0,0,1]                        
    return newArr

def load_model():
    with open('data/saved_data.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

modelo = data["model"]
transdict = data["dict"]

def show_predict_page():
    st.title("Previsão de ataque cardíaco")

    st.write("""### Preencha as informação a baixo:""")

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

    age = st.number_input("Idade", min_value=18, max_value=100, value=30)
    sex = st.selectbox("Gênero",sex)
    exang = st.selectbox("Angina Induzida por Exercício",("Yes","No"))
    ca = st.number_input("Número de vasos principais", min_value=0, max_value=3, value=0)
    cp = st.selectbox("Tipo de dor no peito",cp)
    trtbps = st.number_input("Pressão Arterial em Repouso", min_value=94, max_value=200, value=120)
    chol =  st.slider("Colestoral em mg/dl", min_value=0., max_value=10., value=3.)
    fbs = st.radio("Açúcar no sangue em jejum > 120 mg/dl",("True","False"))
    restEcg = st.selectbox("Resultados eletrocardiográficos em repouso", rest_ecg)
    thalach = st.slider("Frequência cardíaca máxima alcançada", min_value=70, max_value=200, value=100)

    button = st.button("Enviar")
    if button:
        X = [age,sex,cp,trtbps,chol,fbs,restEcg,thalach,exang,ca]
        X = [transdict.get(i, i) for i in X]
        X = criaDummies(X)
        X = np.asarray(X)
        X = X.reshape(1,-1)

        prediction = modelo.predict(X)
        if (prediction[0] == 0):
            st.subheader("Não há risco de ataque cardíaco")
        else:
            st.subheader("Há risco de ataque cardíaco, recomendamos que procure um médico")
    

