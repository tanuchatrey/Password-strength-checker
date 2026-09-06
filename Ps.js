const passwordInput = document.getElementById("password");
const toggleButton = document.getElementById("togglePassword");

const strengthElement = document.getElementById("strength");
const scoreElement = document.getElementById("score");
const strengthBar = document.getElementById("strengthBar");

const checksElement = document.getElementById("checks");
const suggestionsElement = document.getElementById("suggestions");


toggleButton.addEventListener("click", () => {

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleButton.textContent = "Hide";
    } else {
        passwordInput.type = "password";
        toggleButton.textContent = "Show";
    }

});


passwordInput.addEventListener("input", async () => {

    const password = passwordInput.value;

    if (password.length === 0) {

        strengthElement.textContent = "Not checked";
        scoreElement.textContent = "0";
        strengthBar.style.width = "0%";

        checksElement.innerHTML = "";
        suggestionsElement.innerHTML = "";

        return;
    }

    try {

        const response = await fetch("/check", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                password: password
            })

        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.error);
            return;
        }

        displayResult(result);

    } catch (error) {

        console.error("Error:", error);

    }

});


function displayResult(result) {

    strengthElement.textContent = result.strength;

    scoreElement.textContent = result.score;

    /*
       Maximum score in our current checker is 9.
    */

    const percentage = Math.min(
        (result.score / 9) * 100,
        100
    );

    strengthBar.style.width = percentage + "%";


    checksElement.innerHTML = "";

    result.checks.forEach(check => {

        const li = document.createElement("li");

        if (check.passed) {

            li.textContent = "✓ " + check.name;
            li.classList.add("passed");

        } else {

            li.textContent = "✗ " + check.name;
            li.classList.add("failed");

        }

        checksElement.appendChild(li);

    });


    suggestionsElement.innerHTML = "";

    result.suggestions.forEach(suggestion => {

        const li = document.createElement("li");

        li.textContent = suggestion;

        suggestionsElement.appendChild(li);

    });

}
