import joblib
import pandas as pd

# ==========================
# LOAD MODEL
# ==========================

model = joblib.load("dna_mutation_model.pkl")

print("Loaded Model:")
print(model)

# ==========================
# LOAD ENCODERS
# ==========================

encoders = joblib.load("encoders.pkl")

print("Model loaded successfully!")
print("Encoders loaded successfully!")

# ==========================
# TEST PATIENT
# ==========================

patient = {
    "CHROM": "1",
    "POS": 1737942,
    "REF": "A",
    "ALT": "G",
    "Consequence": "missense_variant",
    "IMPACT": "MODERATE",
    "SYMBOL": "GNB1",
    "CADD_PHRED": 28.1,
}

# ==========================
# ENCODE PATIENT DATA
# ==========================

patient["CHROM"] = encoders["CHROM"].transform([patient["CHROM"]])[0]
patient["REF"] = encoders["REF"].transform([patient["REF"]])[0]
patient["ALT"] = encoders["ALT"].transform([patient["ALT"]])[0]
patient["Consequence"] = encoders["Consequence"].transform([patient["Consequence"]])[0]
patient["IMPACT"] = encoders["IMPACT"].transform([patient["IMPACT"]])[0]
patient["SYMBOL"] = encoders["SYMBOL"].transform([patient["SYMBOL"]])[0]

print("\nEncoded Patient:")
print(patient)

# ==========================
# CREATE DATAFRAME
# ==========================

patient_df = pd.DataFrame([patient])

print("\nPatient DataFrame:")
print(patient_df)

# ==========================
# PREDICT
# ==========================

prediction = model.predict(patient_df)

print("\nRaw Prediction:")
print(prediction)

if hasattr(model, "predict_proba"):
    probabilities = model.predict_proba(patient_df)

    print("\nPrediction Probabilities:")
    print(probabilities)

    if prediction[0] == 1:
        print("\n⚠️ Prediction: Harmful Mutation")
    else:
        print("\n✅ Prediction: Safe Mutation")
