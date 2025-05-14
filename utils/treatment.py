def get_treatment_plan(disease, severity_score, temperature, humidity, soil_type, growth_stage):
    """
    Generates a treatment plan based on disease, severity, and environmental conditions.
    """

    plan = {
        "message": "No specific treatment available.",
        "actions": "None",
        "products": "None",
        "frequency": "Not applicable",
        "safety": "N/A"
    }

    # Determine environmental risk
    if temperature < 15 or humidity > 85:
        env_risk = "high"
    elif 15 <= temperature <= 28 and 50 <= humidity <= 85:
        env_risk = "moderate"
    else:
        env_risk = "low"

    # Disease-specific treatment logic
    if disease == "Apple_Black_rot":
        if severity_score > 60 or env_risk == "high":
            plan.update({
                "message": "Severe Black Rot with high environmental risk.",
                "actions": "Prune infected limbs. Apply strong systemic fungicide. Consider soil amendment if clay-based.",
                "products": "Dithane M-45, Myclobutanil.",
                "frequency": "Every 5 days for 3–4 applications.",
                "safety": "Use full PPE; avoid spraying near water sources."
            })
        elif 30 < severity_score <= 60 or env_risk == "moderate":
            plan.update({
                "message": "Moderate Black Rot detected.",
                "actions": "Remove infected fruits, apply curative fungicide.",
                "products": "Thiophanate-methyl, Mancozeb.",
                "frequency": "Weekly for 3 weeks.",
                "safety": "Wear gloves, mask, and goggles."
            })
        else:
            plan.update({
                "message": "Mild Black Rot. Early intervention is sufficient.",
                "actions": "Prune lightly, apply copper-based spray.",
                "products": "Copper fungicide, organic neem-based sprays.",
                "frequency": "Every 10–14 days.",
                "safety": "Standard safety gear recommended."
            })

    elif disease == "Apple_cedar_Apple_rust":
        if env_risk == "high" and soil_type in ["clay", "sandy"]:
            plan.update({
                "message": "Rust risk high due to humidity and soil type.",
                "actions": "Apply systemic fungicide, remove nearby cedar hosts, improve soil drainage.",
                "products": "Propiconazole, Trifloxystrobin.",
                "frequency": "Every 7 days during high humidity.",
                "safety": "Use full PPE, avoid application before rain."
            })
        elif severity_score > 50:
            plan.update({
                "message": "Rust moderately spread.",
                "actions": "Apply protectant fungicide, prune infected areas.",
                "products": "Myclobutanil, Mancozeb.",
                "frequency": "Every 10 days.",
                "safety": "Avoid skin contact; wear long sleeves and gloves."
            })
        else:
            plan.update({
                "message": "Early-stage rust. Preventive action recommended.",
                "actions": "Apply light fungicide and monitor.",
                "products": "Myclobutanil.",
                "frequency": "Every 14 days.",
                "safety": "Basic safety gear recommended."
            })

    elif disease == "Apple_scab":
        if growth_stage == "flowering" and env_risk != "low":
            plan.update({
                "message": "Scab during flowering. Sensitive stage — careful control needed.",
                "actions": "Use flowering-safe fungicides and increase airflow around trees.",
                "products": "Captan, Dodine.",
                "frequency": "Every 10 days until fruit set.",
                "safety": "Do not spray directly on flowers. Use gloves and face shield."
            })
        elif severity_score > 60:
            plan.update({
                "message": "Severe scab outbreak.",
                "actions": "Apply systemic fungicide, remove infected foliage.",
                "products": "Difenoconazole, Trifloxystrobin.",
                "frequency": "Every 5 days for 3 rounds.",
                "safety": "Full PPE required due to high volume spray."
            })
        else:
            plan.update({
                "message": "Initial signs of scab.",
                "actions": "Use preventive sprays and remove debris.",
                "products": "Mancozeb, sulfur-based fungicide.",
                "frequency": "Every 10–14 days.",
                "safety": "Gloves and mask recommended."
            })

    elif disease == "Apple_healthy":
        plan.update({
            "message": "No disease detected. Conditions are stable.",
            "actions": "Continue integrated pest and disease management (IPDM).",
            "products": "Optional: Compost teas, neem oil (preventive).",
            "frequency": "Monitor weekly.",
            "safety": "Maintain standard field hygiene."
        })

    return plan
