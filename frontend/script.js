document.addEventListener("DOMContentLoaded", () => {

    const analysisButtons = document.querySelectorAll(
        'a[href="#"], .primary-button, .cta-button'
    );

    analysisButtons.forEach((button) => {

        const buttonText = button.textContent
            .trim()
            .toLowerCase();

        if (
            buttonText.includes("start analysis") ||
            buttonText.includes("start exercise analysis") ||
            buttonText.includes("start your journey")
        ) {

            button.addEventListener("click", async (event) => {

                event.preventDefault();

                const originalText = button.textContent;

                button.textContent = "Starting Analysis...";
                button.style.pointerEvents = "none";

                try {

                    const response = await fetch("/start-analysis");

                    const data = await response.json();

                    if (data.success) {

                        button.textContent = "Analysis Started";

                        setTimeout(() => {
                            button.textContent = originalText;
                            button.style.pointerEvents = "auto";
                        }, 2500);

                    } else {

                        alert(
                            "Unable to start exercise analysis.\n\n" +
                            data.message
                        );

                        button.textContent = originalText;
                        button.style.pointerEvents = "auto";
                    }

                } catch (error) {

                    console.error(
                        "FormFit analysis error:",
                        error
                    );

                    alert(
                        "Could not connect to the FormFit AI backend.\n\n" +
                        "Make sure the Flask server is running."
                    );

                    button.textContent = originalText;
                    button.style.pointerEvents = "auto";
                }

            });

        }

    });

});PYTHON