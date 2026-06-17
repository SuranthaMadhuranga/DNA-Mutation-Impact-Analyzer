import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")


def explain_mutation(patient, prediction, confidence):

    result = "Harmful Mutation" if prediction == 1 else "Safe Mutation"

    prompt = f"""
    You are a computational biology expert.

    Patient Mutation Information:

        Gene: {patient['SYMBOL']}
        Chromosome: {patient['CHROM']}
        Mutation: {patient['REF']} -> {patient['ALT']}
        Consequence: {patient['Consequence']}
        Impact: {patient['IMPACT']}
        CADD Score: {patient['CADD_PHRED']}

        Machine Learning Result:
            Prediction: {result}
            Confidence: {confidence:.2f}%

            Explain:

                1. What this mutation means
                2. Why it may be harmful or safe
                3. Importance of the CADD score
                4. Clinical interpretation

                Use simple language.

                Maximum 150 words.
                """

    response = model.generate_content(prompt)

    return response.text
