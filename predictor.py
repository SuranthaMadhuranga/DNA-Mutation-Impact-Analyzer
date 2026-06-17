import joblib
import pandas as pd

model = joblib.load("dna_mutation_model.pkl")
encoders = joblib.load("encoders.pkl")


def predict_mutation(patient):

    encoded_patient = patient.copy()

    encoded_patient["CHROM"] = encoders["CHROM"].transform([encoded_patient["CHROM"]])[
        0
    ]

    encoded_patient["REF"] = encoders["REF"].transform([encoded_patient["REF"]])[0]

    encoded_patient["ALT"] = encoders["ALT"].transform([encoded_patient["ALT"]])[0]

    encoded_patient["Consequence"] = encoders["Consequence"].transform(
        [encoded_patient["Consequence"]]
    )[0]

    encoded_patient["IMPACT"] = encoders["IMPACT"].transform(
        [encoded_patient["IMPACT"]]
    )[0]

    encoded_patient["SYMBOL"] = encoders["SYMBOL"].transform(
        [encoded_patient["SYMBOL"]]
    )[0]

    encoded_patient["POS"] = int(encoded_patient["POS"])
    encoded_patient["CADD_PHRED"] = float(encoded_patient["CADD_PHRED"])

    patient_df = pd.DataFrame([encoded_patient])

    prediction = model.predict(patient_df)[0]

    probability = model.predict_proba(patient_df)[0]

    return prediction, probability
