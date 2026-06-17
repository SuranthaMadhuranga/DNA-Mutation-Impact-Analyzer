import streamlit as st
from pdf_reader import extract_text
from parser import extract_features
from predictor import predict_mutation
from gemini_explainer import explain_mutation
from io import BytesIO
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


st.set_page_config(
    page_title="DNA Mutation Impact Analyzer", page_icon="🧬", layout="wide"
)

st.title("🧬 DNA Mutation Impact Analyzer")
st.write("Upload a patient DNA mutation report in PDF format.")

uploaded_file = st.file_uploader("📄 Upload Patient PDF", type=["pdf"])

if uploaded_file:

    # Extract PDF text
    text = extract_text(uploaded_file)

    # Extract mutation features
    patient = extract_features(text)

    # Show extracted PDF text
    with st.expander("📄 Extracted PDF Text"):
        st.text(text)

    # Mutation Summary
    st.subheader("🧬 Mutation Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Gene", patient.get("SYMBOL", "N/A"))

    with col2:
        st.metric("Chromosome", patient.get("CHROM", "N/A"))

    col3, col4 = st.columns(2)

    with col3:
        st.metric("CADD Score", patient.get("CADD_PHRED", "N/A"))

    with col4:

        impact = patient.get("IMPACT", "N/A")

        if impact == "HIGH":
            color = "#ef4444"
        elif impact == "MODERATE":
            color = "#f59e0b"
        else:
            color = "#22c55e"

        st.markdown(
            f"""
            <p style="color:#94a3b8;font-size:14px;font-weight:500;">
                Impact Level
            </p>

            <p style="color:{color};font-size:42px;font-weight:800;margin-top:-10px;">
                {impact}
            </p>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
            <div class="summary-card">
            <b>Mutation:</b> {patient.get('REF', 'N/A')} → {patient.get('ALT', 'N/A')}
            <br><br>
            <b>Consequence:</b> {patient.get('Consequence', 'N/A')}
            </div>
            """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Analyze Mutation
    if st.button("🔬 Analyze Mutation"):

        prediction, probability = predict_mutation(patient)

        harmful_probability = probability[1] * 100

        if harmful_probability >= 85:
            risk_level = "🔴 HIGH"
        elif harmful_probability >= 60:
            risk_level = "🟠 MODERATE"
        else:
            risk_level = "🟢 LOW"

        st.subheader("🧠 AI Prediction")

        if prediction == 1:
            st.error("⚠ Harmful Mutation Detected")
        else:
            st.success("✅ Safe Mutation")

        st.metric("Confidence", f"{harmful_probability:.2f}%")
        st.progress(harmful_probability / 100)
        if harmful_probability >= 85:
            st.error(f"Risk Level: {risk_level}")
        elif harmful_probability >= 60:
            st.warning(f"Risk Level: {risk_level}")
        else:
            st.success(f"Risk Level: {risk_level}")

        st.subheader("🧬 AI Clinical Explanation")

        try:
            with st.spinner("Analyzing mutation with Gemini..."):
                explanation = explain_mutation(patient, prediction, harmful_probability)

            st.markdown(
                f"""
                <div class="explanation-card">
                {explanation}
                 </div>
                """,
                unsafe_allow_html=True,
            )

            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "CustomTitle",
                parent=styles["Title"],
                textColor=colors.HexColor("#2563EB"),
                fontSize=24,
                spaceAfter=20,
            )

            heading_style = ParagraphStyle(
                "CustomHeading",
                parent=styles["Heading2"],
                textColor=colors.HexColor("#06B6D4"),
            )

            footer_style = ParagraphStyle(
                "Footer",
                parent=styles["Italic"],
                textColor=colors.grey,
            )
            content = []

            # PDF topic

            content.append(
                Paragraph(
                    "🧬 DNA Mutation Impact Analysis Report",
                    title_style,
                )
            )
            content.append(Spacer(1, 20))

            content.append(
                Paragraph(
                    f"Report Date: {datetime.now().strftime('%Y-%m-%d')}",
                    styles["Normal"],
                )
            )
            content.append(Spacer(1, 15))

            # Patient Information

            content.append(
                Paragraph(
                    "Patient Information",
                    heading_style,
                )
            )

            content.append(
                Paragraph(f"Gene: {patient.get('SYMBOL','N/A')}", styles["Normal"])
            )

            content.append(
                Paragraph(f"Chromosome: {patient.get('CHROM','N/A')}", styles["Normal"])
            )

            content.append(
                Paragraph(f"Impact: {patient.get('IMPACT','N/A')}", styles["Normal"])
            )

            content.append(
                Paragraph(
                    f"CADD Score: {patient.get('CADD_PHRED','N/A')}", styles["Normal"]
                )
            )
            content.append(Spacer(1, 15))

            ## Prediction Results##
            content.append(
                Paragraph(
                    "Prediction Results",
                    heading_style,
                )
            )

            content.append(
                Paragraph(
                    f"Prediction: {'Harmful Mutation' if prediction == 1 else 'Safe Mutation'}",
                    styles["Normal"],
                )
            )

            content.append(
                Paragraph(f"Confidence: {harmful_probability:.2f}%", styles["Normal"])
            )

            content.append(Paragraph(f"Risk Level: {risk_level}", styles["Normal"]))
            content.append(Spacer(1, 25))

            ##AI Clinical Explanation##
            content.append(
                Paragraph(
                    "AI Clinical Explanation",
                    heading_style,
                )
            )

            clean_explanation = explanation.replace("**", "").replace("#", "")

            content.append(Paragraph(clean_explanation, styles["BodyText"]))

            content.append(Spacer(1, 20))

            content.append(
                Paragraph(
                    "Generated by DNA Mutation Impact Analyzer | Powered by AI & Machine Learning",
                    footer_style,
                )
            )

            doc.build(content)

            pdf_buffer.seek(0)

            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer.getvalue(),
                file_name="DNA_Mutation_Report.pdf",
                mime="application/pdf",
            )

        except Exception as e:
            st.error(f"Gemini Error: {str(e)}")
else:
    st.info("Please upload a patient PDF report.")
