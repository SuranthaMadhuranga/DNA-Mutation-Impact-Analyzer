from predictor import predict_mutation

patient = {
    "CHROM": "1",
    "POS": "1737942",
    "REF": "A",
    "ALT": "G",
    "Consequence": "missense_variant",
    "IMPACT": "MODERATE",
    "SYMBOL": "GNB1",
    "CADD_PHRED": "28.1",
}

prediction, probability = predict_mutation(patient)

print(prediction)
print(probability)
