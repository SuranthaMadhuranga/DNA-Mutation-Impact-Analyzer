import re


def extract_features(text):

    patient = {}

    patient["CHROM"] = re.search(r"CHROM:\s*(.+)", text).group(1).strip()
    patient["POS"] = re.search(r"POS:\s*(.+)", text).group(1).strip()
    patient["REF"] = re.search(r"REF:\s*(.+)", text).group(1).strip()
    patient["ALT"] = re.search(r"ALT:\s*(.+)", text).group(1).strip()
    patient["Consequence"] = re.search(r"Consequence:\s*(.+)", text).group(1).strip()
    patient["IMPACT"] = re.search(r"IMPACT:\s*(.+)", text).group(1).strip()
    patient["SYMBOL"] = re.search(r"SYMBOL:\s*(.+)", text).group(1).strip()
    patient["CADD_PHRED"] = re.search(r"CADD_PHRED:\s*(.+)", text).group(1).strip()

    print("\n========== EXTRACTED FEATURES ==========")
    print(patient)
    print("========================================\n")

    return patient
