import streamlit as st
import pickle
import pandas as pd

# Load the processed dataset
pickle_file_path = "soil_data_processed.pkl"
with open(pickle_file_path, "rb") as file:
    classified_data = pickle.load(file)

# Define selected features for input
selected_features = [
    "B ppm", "CACO3 %", "Fe ppm",  "Mg ppm", "Mn ppm", 
    "O.M. %", "P ppm", "Zn ppm", "pH"
]

# Load thresholds
low_threshold = classified_data[selected_features].quantile(0.33)
high_threshold = classified_data[selected_features].quantile(0.66)
excess_threshold = classified_data[selected_features].quantile(0.90)  # Setting excess limit at the 90th percentile

def classify_soil_levels(value, low, high, excess, feature):
    if feature == "pH":
        if value > 14:
            return "Excess"
        elif value < 5.5:
            return "Deficient"
        elif value >= 5.5 and value <= 7.5:
            return "Moderate"
        elif value > 7.5 and value <= 14:
            return "Sufficient"
    else:
        if value <= low:
            return "Deficient"
        elif value >= excess:
            return "Excess"
        elif value >= high:
            return "Sufficient"
        else:
            return "Moderate"

def suggest_crops(classification_results):
    # Define crop recommendations based on soil nutrient status
    crop_recommendations = {
        "Deficient": ["Legumes", "Barley", "Peas", "Millets", "Oats"],
        "Moderate": ["Rice", "Wheat", "Corn", "Soybean", "Groundnut"],
        "Sufficient": ["Sugarcane", "Cotton", "Banana", "Sunflower", "Tobacco"],
        "Excess": ["Water-resistant crops", "Jute", "Papaya", "Sesame", "Mustard"]
    }
    
    # Count classification occurrences
    status_counts = {status: list(classification_results.values()).count(status) for status in ["Deficient", "Moderate", "Sufficient", "Excess"]}
    
    # Determine the dominant soil classification
    dominant_status = max(status_counts, key=status_counts.get)
    return crop_recommendations.get(dominant_status, [])

st.title("Soil Classification App")

st.write("Enter the soil composition values to classify them as Sufficient, Deficient, Moderate, or Excess.")

# User input form
user_input = {}
for feature in selected_features:
    user_input[feature] = st.number_input(f"{feature}", min_value=0.0, format="%.4f")

if st.button("Classify Soil"):
    result = {}
    for feature in selected_features:
        result[feature] = classify_soil_levels(user_input[feature], low_threshold[feature], high_threshold[feature], excess_threshold[feature], feature)
    
    st.write("### Classification Results:")
    st.json(result)
    
    # Suggest crops based on classification
    suggested_crops = suggest_crops(result)
    st.write("### Recommended Crops:")
    st.write(", ".join(suggested_crops) if suggested_crops else "No specific recommendation.")
