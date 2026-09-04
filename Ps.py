from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# A small list for demonstration.
# In a real application, use a much larger compromised-password database.
COMMON_PASSWORDS = {
    "123456",
    "password",
    "123456789",
    "12345678",
    "qwerty",
    "abc123",
    "password123",
    "admin",
    "letmein",
    "welcome",
    "iloveyou",
}


def check_password(password):
    score = 0
    suggestions = []
    checks = []

    # Length
    if len(password) >= 12:
        score += 2
        checks.append({
            "name": "At least 12 characters",
            "passed": True
        })
    elif len(password) >= 8:
        score += 1
        checks.append({
            "name": "At least 8 characters",
            "passed": True
        })
        suggestions.append("Use at least 12 characters.")
    else:
        checks.append({
            "name": "At least 8 characters",
            "passed": False
        })
        suggestions.append("Use at least 8 characters, preferably 12+.")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
        checks.append({
            "name": "Contains uppercase letter",
            "passed": True
        })
    else:
        checks.append({
            "name": "Contains uppercase letter",
            "passed": False
        })
        suggestions.append("Add at least one uppercase letter.")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
        checks.append({
            "name": "Contains lowercase letter",
            "passed": True
        })
    else:
        checks.append({
            "name": "Contains lowercase letter",
            "passed": False
        })
        suggestions.append("Add at least one lowercase letter.")

    # Number
    if re.search(r"\d", password):
        score += 1
        checks.append({
            "name": "Contains a number",
            "passed": True
        })
    else:
        checks.append({
            "name": "Contains a number",
            "passed": False
        })
        suggestions.append("Add at least one number.")

    # Special character
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
        checks.append({
            "name": "Contains special character",
            "passed": True
        })
    else:
        checks.append({
            "name": "Contains special character",
            "passed": False
        })
        suggestions.append("Add a special character such as !, @, # or $.")

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        score = 0
        checks.append({
            "name": "Not a common password",
            "passed": False
        })
        suggestions.append("This is a commonly used password. Choose something unique.")
    else:
        score += 1
        checks.append({
            "name": "Not a common password",
            "passed": True
        })

    # Repeated characters
    if re.search(r"(.)\1\1", password):
        checks.append({
            "name": "Avoids repeated characters",
            "passed": False
        })
        suggestions.append("Avoid repeating the same character three or more times.")
    else:
        score += 1
        checks.append({
            "name": "Avoids repeated characters",
            "passed": True
        })

    # Sequential patterns
    sequences = [
        "1234",
        "2345",
        "3456",
        "4567",
        "5678",
        "6789",
        "abcd",
        "bcde",
        "cdef",
        "qwer"
    ]

    if any(sequence in password.lower() for sequence in sequences):
        checks.append({
            "name": "Avoids predictable sequences",
            "passed": False
        })
        suggestions.append("Avoid predictable sequences such as 1234 or abcd.")
    else:
        score += 1
        checks.append({
            "name": "Avoids predictable sequences",
            "passed": True
        })

    # Determine strength
    if score <= 3:
        strength = "Weak"
    elif score <= 5:
        strength = "Moderate"
    elif score <= 7:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        "score": score,
        "strength": strength,
        "checks": checks,
        "suggestions": suggestions
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()

    if not data or "password" not in data:
        return jsonify({
            "error": "Password is required."
        }), 400

    password = data["password"]

    if not isinstance(password, str):
        return jsonify({
            "error": "Password must be text."
        }), 400

    # Don't log or store the password.
    result = check_password(password)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
