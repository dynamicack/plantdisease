def get_pesticide_recommendation(disease, severity_score):
    """
    Returns pesticide recommendation based on disease and severity.
    """
    recommendation = {
        "message": "No pesticide recommendation available.",
        "strength": "N/A",
        "products": "N/A",
        "frequency": "N/A",
        "safety": "N/A"
    }

    if disease == "Apple_Black_rot":
        if severity_score <= 30:
            recommendation.update({
                "message": "Mild infection detected. Early control advised.",
                "strength": "1.5 ml per liter of water",
                "products": "Captan 50 WP, Ziram 76DF",
                "frequency": "Spray once every 10 days",
                "safety": "Wear gloves and a mask. Avoid spraying during windy conditions. Wash hands after use."
            })
        elif severity_score <= 60:
            recommendation.update({
                "message": "Moderate infection. Start immediate treatment.",
                "strength": "2 ml per liter of water",
                "products": "Thiophanate-methyl, Myclobutanil",
                "frequency": "Spray every 7 days for 2 weeks",
                "safety": "Avoid eye and skin contact. Wash equipment thoroughly after spraying."
            })
        else:
            recommendation.update({
                "message": "Severe infection. Aggressive pesticide plan required.",
                "strength": "2.5–3 ml per liter",
                "products": "Copper-based fungicides, Mancozeb, or Dithane M-45",
                "frequency": "Spray every 5 days for 3 applications",
                "safety": "Use full PPE. Keep children and animals away for 24 hours."
            })

    elif disease == "Apple_cedar_Apple_rust":
        if severity_score <= 30:
            recommendation.update({
                "message": "Low-level rust. Preventative fungicide recommended.",
                "strength": "1–1.5 ml per liter",
                "products": "Myclobutanil, Propiconazole",
                "frequency": "Apply once every 14 days",
                "safety": "Apply during early morning or evening. Wear long sleeves and goggles."
            })
        elif severity_score <= 60:
            recommendation.update({
                "message": "Moderate rust. Begin treatment promptly.",
                "strength": "2 ml per liter",
                "products": "Propiconazole, Mancozeb",
                "frequency": "Apply weekly for 3 weeks",
                "safety": "Avoid inhaling spray mist. Store chemicals in original containers."
            })
        else:
            recommendation.update({
                "message": "High infection rate. Control immediately.",
                "strength": "2.5–3 ml per liter",
                "products": "Trifloxystrobin + Tebuconazole (e.g., Nativo)",
                "frequency": "Apply every 5 days for 3 cycles",
                "safety": "Use full PPE. Do not spray during pollination period."
            })

    elif disease == "Apple_scab":
        if severity_score <= 30:
            recommendation.update({
                "message": "Initial scab signs. Preventive action required.",
                "strength": "1.5 ml per liter",
                "products": "Captan or Mancozeb",
                "frequency": "Apply every 10–14 days",
                "safety": "Ensure foliage is dry before spraying. Wear rubber gloves and mask."
            })
        elif severity_score <= 60:
            recommendation.update({
                "message": "Moderate scab. Apply curative fungicides.",
                "strength": "2 ml per liter",
                "products": "Dodine or Trifloxystrobin",
                "frequency": "Apply weekly for 3–4 weeks",
                "safety": "Avoid contact with eyes. Wash sprayer after use."
            })
        else:
            recommendation.update({
                "message": "Advanced scab detected. Use systemic fungicides.",
                "strength": "3 ml per liter",
                "products": "Difenoconazole, Copper Oxychloride",
                "frequency": "Spray every 4–5 days until symptoms reduce",
                "safety": "Apply with respirator. Do not allow spray to drift into water sources."
            })

    elif disease == "Apple_healthy":
        recommendation.update({
            "message": "Plant is healthy. No pesticide needed.",
            "strength": "None",
            "products": "None",
            "frequency": "Not applicable",
            "safety": "Continue regular inspection and maintain hygiene."
        })

    return recommendation
