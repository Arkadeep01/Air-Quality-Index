import streamlit as st
import numpy as np
import pickle
import os

# Hide Streamlit UI elements
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load AQI Model (ARIMA)
model_path = r"C:\Users\LENOVO\OneDrive\AICTE\Air Quality Index Prediction\Air Quality Index Prediction Model.pkl"

if os.path.exists(model_path):
    try:
        with open(model_path, "rb") as model_file:
            aqi_model = pickle.load(model_file)
        st.success("✅ Model loaded successfully!")
    except Exception as e:
        st.error(f"⚠️ Model loading failed: {str(e)}")
        aqi_model = None
else:
    st.error("⚠️ AQI model not found! Please check the file path.")
    aqi_model = None

# Sidebar Navigation
st.sidebar.title("Air Quality Prediction")
app_mode = st.sidebar.selectbox("Choose an option", ["Home", "Prediction"])

# Home Page
if app_mode == "Home":
    st.markdown("""
        <div style="text-align: center;">
            <h2>🌍 Welcome to the AI-Powered Air Quality Index Prediction System</h2>
        </div>
    """, unsafe_allow_html=True)

    st.write("""
        Monitoring air quality is crucial for maintaining a healthy environment.  

        ### ✅ Why is Air Quality Important?
        - **Better Health**: Reduces respiratory issues.
        - **Environmental Protection**: Helps control pollution levels.
        - **Informed Decisions**: Allows authorities to take necessary precautions.

        ### 🛠 Key Factors Affecting Air Quality:
        - **PM2.5 & PM10 Levels** 🌫
        - **Carbon Monoxide (CO)** 🚗
        - **Sulfur Dioxide (SO₂)** 🏭
        - **Nitrogen Dioxide (NO₂)** 🌆
        - **Ozone (O₃) Levels** 🌞

        ⚠️ This AI-based prediction is for reference only. Please refer to official sources for accurate AQI data.
    """)

# Prediction Page
if app_mode == "Prediction":
    st.title('🌍 Air Quality Index Prediction')
    st.write("Enter the environmental factors to predict the AQI level:")

    # Define the input features (all relevant air quality parameters)
    features = ["PM2.5", "PM10", "CO", "NO2", "SO2", "O3", "Toulene"]

    input_data = {}
    for feature in features:
        input_data[feature] = st.number_input(feature, key=feature, step=0.1)

    if aqi_model:
        try:
            # Prepare input data for ARIMA (Convert all inputs into a meaningful 1D time-series format)
            input_array = np.array(list(input_data.values())).reshape(-1)

            if st.button('Predict AQI'):
                # ARIMA expects a 1D time-series, so we pass a proper array
                prediction = aqi_model.predict(len(input_array))[-1]  # Predicting based on recent input values

                # AQI category interpretation
                if prediction <= 50:
                    category = "Good 😊"
                    color = "green"
                elif prediction <= 100:
                    category = "Moderate 🙂"
                    color = "yellow"
                elif prediction <= 150:
                    category = "Unhealthy for Sensitive Groups 😷"
                    color = "orange"
                elif prediction <= 200:
                    category = "Unhealthy 😨"
                    color = "red"
                elif prediction <= 300:
                    category = "Very Unhealthy ☠️"
                    color = "purple"
                else:
                    category = "Hazardous ⚠️"
                    color = "maroon"

                # Display results
                st.markdown(f"""
                    <div style="border-radius:10px;padding:15px;background-color:{color};text-align:center;">
                        <h2>AQI Prediction: {prediction:.2f}</h2>
                        <h3>Category: {category}</h3>
                    </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Prediction error: {str(e)}")
    else:
        st.error("🚫 Model is not loaded. Please check for errors.")
