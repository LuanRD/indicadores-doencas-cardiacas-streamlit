import pandas as pd
import pickle
import streamlit as st

pipeline = pickle.load(open('models/pipeline.pkl', 'rb'))

columns = ['BMI', 'Smoking', 'AlcoholDrinking', 'Stroke', 'PhysicalHealth',
           'MentalHealth', 'DiffWalking', 'Sex', 'AgeCategory', 'Race', 'Diabetic',
           'PhysicalActivity', 'GenHealth', 'SleepTime', 'Asthma', 'KidneyDisease',
           'SkinCancer']


def predict_disease(inputs):
    values = []

    for i, j in enumerate(inputs):
        i = []
        i.append(j)
        values.append(i)

    zip_obj = zip(columns, values)
    df = pd.DataFrame(dict(zip_obj))

    binary = ['Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking', 'PhysicalActivity', 'Asthma', 'KidneyDisease', 'SkinCancer']

    for column in df[binary]:
        df[column] = df[column].map({'Não': 'No', 'Sim': 'Yes'})

    df['Sex'] = df['Sex'].map({'Masculino': 'Male', 'Feminino': 'Female'})
    df['Diabetic'] = df['Diabetic'].map({'Não': 'No', 'Sim': 'Yes', 'Pré-diabetes': 'No, borderline diabetes', 'Sim (durante a gravidez)': 'Yes (during pregnancy)'})
    df['Race'] = df['Race'].map({'Branco': 'White', 'Preto': 'Black', 'Asiático': 'Asian', 'Indígena': 'American Indian/Alaskan Native', 'Pardo': 'Hispanic', 'Outro': 'Other'})
    df['GenHealth'] = df['GenHealth'].map({'Muito boa': 'Very good', 'Boa': 'Good', 'Regular': 'Fair', 'Ruim': 'Poor', 'Excelente': 'Excellent'})

    prediction = pipeline.predict(df)
    probability = pipeline.predict_proba(df)

    if prediction[0] == 0:
        return f'Resultado: Você provavelmente não tem doenças cardíacas. Probabilidade = {(probability[0][1] * 100):.2f}%'
    else:
        return f'Resultado: Você provavelmente tem doenças cardíacas. Consulte-se com um médico. Probabilidade = {(probability[0][1] * 100):.2f}%'


def main():
    st.title('Predição de Doenças Cardíacas')

    st.subheader('Esse aplicativo foi criado baseado nos dados fornecidos pelo CDC americano em uma pesquisa anual. A partir desses dados, foi criado um modelo de Machine Learning que buscou prever a saúde cardíaca das pessoas à partir de informações pessoais. Esse projeto não tem o intuito de possuir cunho científico.', anchor=None)

    Sex = st.radio("Qual o seu gênero de nascimento?", ("Masculino", "Feminino"))
    Race = st.radio("Selecione sua cor/etnia:", ("Indígena", "Asiático", "Preto", "Pardo", "Branco", "Outro"))
    AgeCategory = st.radio("Selecione sua faixa etária:", ("18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 or older"))
    Altura = st.number_input("Insira a sua altura (m)", 0.01, 2.10)
    Peso = st.number_input("Insira o seu peso (kg)", 0.01, 300.00)
    BMI = Peso/(Altura**2)
    Smoking = st.radio("Você já fumou pelo menos 100 cigarros durante sua vida?", ("Não", "Sim"))
    AlcoholDrinking = st.radio("Você consome álcool muito frequentemente? [Masculino - mais de 14 drinks/semana / Feminino - mais de 7 drinks/semana]", ("Não", "Sim"))
    PhysicalHealth = st.number_input("Considerando os últimos 30 dias, em quantos deles sua saúde física não esteve boa?", 0, 30)
    MentalHealth = st.number_input("Considerando os últimos 30 dias, em quantos deles sua saúde mental não esteve boa?", 0, 30)
    DiffWalking = st.radio("Você tem grande dificuldade para andar ou subir escadas?", ("Não", "Sim"))
    Stroke = st.radio("Já teve um derrame?", ("Não", "Sim"))   
    Diabetic = st.radio("Você tem diabetes?", ("Não", "Pré-diabetes", "Sim", "Sim (durante a gravidez)"))
    PhysicalActivity = st.radio(
        "Nos últimos 30 dias, você praticou alguma atividade física (excetuando seu trabalho)?",
        ("Não", "Sim"))
    GenHealth = st.radio("Você diria que, no geral, sua saúde é:",
                         ("Ruim", "Regular", "Boa", "Muito boa", "Excelente"))
    SleepTime = st.number_input("Em média, quantas horas de sono você tem em um período de 24 horas?", 0, 24)
    Asthma = st.radio("Você tem asma?", ("Não", "Sim"))
    KidneyDisease = st.radio(
        "Excluindo pedra nos rins, infecção na bexiga ou incontinência, você tem/teve alguma doença renal?",
        ("Não", "Sim"))
    SkinCancer = st.radio("Você tem/teve câncer de pele?", ("Não", "Sim"))

    diagnosis = ''

    if st.button('Resultado'):
        diagnosis = predict_disease(
            [BMI, Smoking, AlcoholDrinking, Stroke, PhysicalHealth, MentalHealth, DiffWalking, Sex, AgeCategory,
             Race, Diabetic, PhysicalActivity, GenHealth, SleepTime, Asthma, KidneyDisease, SkinCancer])

        st.success(diagnosis)


if __name__ == '__main__':
    main()
