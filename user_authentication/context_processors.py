

def password_validation(request):
    context = {}
    context["upper_case"] = "?=.*[A-Z]"
    context["lower_case"] = "?=.*[a-z]"
    context["password_digit"] = "?=.*[0-9]"
    context["special_character"] = "?=.*[@#$%&]"
    return context