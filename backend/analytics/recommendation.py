class RecommendationEngine:

    RECOMMENDATIONS = {

        "Obesity_W": [
            "Increase physical activity awareness for women",
            "Strengthen nutrition counselling at PHCs",
            "Promote healthy diet campaigns"
        ],

        "Obesity_M": [
            "Launch workplace wellness programmes",
            "Promote regular BMI screening",
            "Increase public fitness initiatives"
        ],

        "Anaemia_Child": [
            "Expand Iron and Folic Acid supplementation",
            "Improve Mid-Day Meal nutrition",
            "Conduct school nutrition awareness campaigns"
        ],

        "Anaemia_W": [
            "Increase anaemia screening among women",
            "Provide Iron and Folic Acid tablets",
            "Promote maternal nutrition programmes"
        ],

        "BloodSugar_W": [
            "Increase diabetes screening",
            "Promote healthy lifestyle awareness",
            "Strengthen NCD clinics"
        ],

        "BloodSugar_M": [
            "Organize diabetes health camps",
            "Encourage annual blood sugar testing",
            "Promote exercise programmes"
        ],

        "Hypertension_W": [
            "Increase blood pressure screening",
            "Promote low-salt diet awareness",
            "Strengthen community health monitoring"
        ],

        "Hypertension_M": [
            "Expand hypertension screening camps",
            "Promote lifestyle modification",
            "Increase cardiovascular awareness"
        ]
    }

    @staticmethod
    def get_recommendations(top_driver, risk_level):

        recommendations = RecommendationEngine.RECOMMENDATIONS.get(
            top_driver,
            ["Detailed health assessment recommended."]
        )

        if risk_level == "Critical":

            recommendations = [
                "Immediate Government Intervention Required"
            ] + recommendations

        return recommendations