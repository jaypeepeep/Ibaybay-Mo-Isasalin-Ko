/* connecting the keyboard to the text area */
const buttons = document.querySelectorAll('.btn')
const textarea = document.querySelector('textarea')

/* when deleting text from the text area */
const delete_button = document.querySelector('.delete')

/* when putting space in the text area */
const space_button = document.querySelector('.space')

// copying output to clipboard

// for the dropdown function
const dropdowns = document.querySelectorAll('.dropdown-container'),
    inputLangDropdown = document.querySelector('#input-script'),
    outputLangDropdown = document.querySelector('#output-script');

// necessary for storing the value to be passed to app.py, also selectedBasedChar for removing the last letter and replacing it with kudlit
let selectedBaseChar = '';
const storedBaybayinChars = [];

/* click event for da script buttons */
buttons.forEach(btn => {
    btn.addEventListener('click', () => {
        const baybayinCharElement = btn.querySelector('.baybayin-char');
        const baybayinKudlitElement = btn.querySelector('.baybayin-kudlit');

        // Check if the elements are present before accessing textContent
        const baybayinCharContent = baybayinCharElement ? baybayinCharElement.textContent : '';
        const baybayinKudlitContent = baybayinKudlitElement ? baybayinKudlitElement.textContent : '';

        textarea.style.fontFamily = "Baybayin";

        // If the base character is not empty, remove the last character
        if (selectedBaseChar) {
            if (['e', 'i', 'o', 'u'].includes(baybayinKudlitContent)) {
                textarea.value = textarea.value.slice(0, -1);
            }
        }

        // Append the new character to the textarea
        textarea.value += baybayinCharContent + baybayinKudlitContent;

        // Update the selected base character
        selectedBaseChar = baybayinCharContent;

        // Store the kudlit nd character individually
        storedBaybayinChars.push(baybayinCharContent);
        storedBaybayinChars.push(baybayinKudlitContent);

        // Pass the values separately to the backend without modifying them
        console.log(textarea.value);
        console.log("Stored Baybayin Chars: " + storedBaybayinChars.join(''));
    });
});


//

document.addEventListener("DOMContentLoaded", function () {
    // Existing keyboard toggle code
    var baybayinKeyboard = document.querySelector('.card-baybayin-keyboard');
    var toggleButton = document.getElementById('keyboard-display');
    const inputLangDropdown = document.getElementById('input-script');

    // Function to update keyboard button state based on selected script
    function updateKeyboardButtonState() {
        const inputSelectedValue = inputLangDropdown.querySelector(".selected-script").dataset.value;

        if (inputSelectedValue === "lat") {
            // Latin script selected - disable keyboard button
            toggleButton.disabled = true;
            toggleButton.classList.add('disabled-button');

            // Hide keyboard if it's currently visible
            if (baybayinKeyboard.classList.contains('visible')) {
                baybayinKeyboard.classList.remove('visible');
            }
        } else {
            // Baybayin script selected - enable keyboard button
            toggleButton.disabled = false;
            toggleButton.classList.remove('disabled-button');
            baybayinKeyboard.classList.toggle('visible');
        }
    }

    // Add click event listener to the toggle button (existing code)
    if (toggleButton) {
        toggleButton.addEventListener('click', function () {
            // Toggle the visibility of the keyboard by adding/removing the 'visible' class
            baybayinKeyboard.classList.toggle('visible');
        });
    }

    // Add listeners to update button state when input script changes
    const inputDropdownOptions = inputLangDropdown.querySelectorAll(".option");
    inputDropdownOptions.forEach(item => {
        item.addEventListener("click", function () {
            // Allow time for the dropdown change to complete
            setTimeout(updateKeyboardButtonState, 50);
        });
    });

    // Also update when swap button is clicked
    const swapButton = document.querySelector(".swap-position");
    if (swapButton) {
        swapButton.addEventListener("click", function () {
            // Allow time for the swap to complete
            setTimeout(updateKeyboardButtonState, 50);
        });
    }
});

//

/* click event for the delete button */
delete_button.addEventListener('click', () => {
    storedBaybayinChars.pop();
    textarea.value = storedBaybayinChars.join('');
    console.log("Existing Array: " + storedBaybayinChars.join(''));
});

let holdDeleter;

delete_button.addEventListener('mousedown', () => {
    holdDeleter = setInterval(() => {
        storedBaybayinChars.pop(); // Delete the last character
        textarea.value = storedBaybayinChars.join(''); // Update the textarea
    }, 100); // Adjust the interval as needed
});

delete_button.addEventListener('mouseup', () => {
    clearInterval(holdDeleter); // Stop the continuous deletion when the button is released
});

// click event for the space
space_button.addEventListener('click', () => {
    textarea.value += '||';
    storedBaybayinChars.push(' ');
})

document.addEventListener("DOMContentLoaded", function () {
    const inputLangDropdown = document.getElementById("input-script");
    const outputLangDropdown = document.getElementById("output-script");
    const inputText = document.getElementById("input-text");
    const outputText = document.getElementById("output-text");
    const swapButton = document.querySelector(".swap-position");

    // Populate dropdowns with language options
    populateDropdown(inputLangDropdown, languages);
    populateDropdown(outputLangDropdown, languages);

    const inputDropdownOptions = inputLangDropdown.querySelectorAll(".option");
    const outputDropdownOptions = outputLangDropdown.querySelectorAll(".option");

    // Function to deactivate all options in a dropdown
    function deactivateOptions(dropdownOptions) {
        dropdownOptions.forEach(option => {
            option.classList.remove("active");
        });
    }

    // Function to swap input and output dropdowns
    function swapDropdowns() {
        // Swap dropdown values
        const tempValue = inputLangDropdown.querySelector(".selected-script").dataset.value;
        inputLangDropdown.querySelector(".selected-script").dataset.value = outputLangDropdown.querySelector(".selected-script").dataset.value;
        outputLangDropdown.querySelector(".selected-script").dataset.value = tempValue;

        // Swap dropdown states
        const tempInnerHTML = inputLangDropdown.querySelector(".selected-script").innerHTML;
        inputLangDropdown.querySelector(".selected-script").innerHTML = outputLangDropdown.querySelector(".selected-script").innerHTML;
        outputLangDropdown.querySelector(".selected-script").innerHTML = tempInnerHTML;

        // Swap active values
        const tempActiveValue = inputLangDropdown.querySelector(".option.active").dataset.value;
        inputLangDropdown.querySelector(".option.active").classList.remove("active");
        outputLangDropdown.querySelector(`.option[data-value="${tempValue}"]`).classList.add("active");

        outputLangDropdown.querySelector(".option.active").classList.remove("active");
        inputLangDropdown.querySelector(`.option[data-value="${tempActiveValue}"]`).classList.add("active");

        inputText.value = "";
        outputText.value = "";

        if (inputLangDropdown.querySelector(".selected-script").dataset.value == "byn") {
            inputText.style.fontFamily = "Baybayin";
            inputText.style.fontSize = "40px";
            outputText.style.fontFamily = "";
            outputText.style.fontSize = "";
        } else {
            outputText.style.fontFamily = "Baybayin";
            outputText.style.fontSize = "40px";
            inputText.style.fontFamily = "";
            inputText.style.fontSize = "";
        }
    }

    swapButton.addEventListener("click", () => {
        swapDropdowns();
    });

    inputLangDropdown.addEventListener("click", () => {
        inputLangDropdown.classList.toggle("active");
    });

    inputDropdownOptions.forEach(item => {
        item.addEventListener("click", () => {
            deactivateOptions(inputDropdownOptions);
            item.classList.add("active");

            const selected = inputLangDropdown.querySelector(".selected-script");
            selected.innerHTML = item.innerHTML;
            selected.dataset.value = item.dataset.value;

            // Find the corresponding option in the output dropdown
            const outputOption = outputLangDropdown.querySelector(`.option[data-value="${item.dataset.value === "lat" ? "byn" : "lat"}"]`);
            deactivateOptions(outputDropdownOptions);
            outputOption.classList.add("active");

            const outputSelected = outputLangDropdown.querySelector(".selected-script");
            outputSelected.innerHTML = outputOption.innerHTML;
            outputSelected.dataset.value = outputOption.dataset.value;

            // Clear input and output text
            inputText.value = "";
            outputText.value = "";

            if (item.dataset.value === "byn") {
                inputText.style.fontFamily = "Baybayin";
                inputText.style.fontSize = "40px";
                outputText.style.fontFamily = "";
                outputText.style.fontSize = "";
            } else {
                outputText.style.fontFamily = "Baybayin";
                outputText.style.fontSize = "40px";
                inputText.style.fontFamily = "";
                inputText.style.fontSize = "";
            }
        });
    });

    outputLangDropdown.addEventListener("click", () => {
        outputLangDropdown.classList.toggle("active");
    });

    outputDropdownOptions.forEach(item => {
        item.addEventListener("click", () => {
            deactivateOptions(outputDropdownOptions);
            item.classList.add("active");

            const selected = outputLangDropdown.querySelector(".selected-script");
            selected.innerHTML = item.innerHTML;
            selected.dataset.value = item.dataset.value;

            // Find the corresponding option in the input dropdown
            const inputOption = inputLangDropdown.querySelector(`.option[data-value="${item.dataset.value === "lat" ? "byn" : "lat"}"]`);
            deactivateOptions(inputDropdownOptions);
            inputOption.classList.add("active");

            const inputSelected = inputLangDropdown.querySelector(".selected-script");
            inputSelected.innerHTML = inputOption.innerHTML;
            inputSelected.dataset.value = inputOption.dataset.value;

            // Clear input and output text
            inputText.value = "";
            outputText.value = "";

            //Make the text field font family changes to baybayin or latin
            if (item.dataset.value === "byn") {
                outputText.style.fontFamily = "Baybayin";
                outputText.style.fontSize = "40px";
                inputText.style.fontFamily = "";
                inputText.style.fontSize = "";
            } else {
                inputText.style.fontFamily = "Baybayin";
                inputText.style.fontSize = "40px";
                outputText.style.fontFamily = "";
                outputText.style.fontSize = "";
            }
        });
    });
});

// Function to populate the dropdown with language options
function populateDropdown(dropdown, languages) {
    const dropdownMenu = dropdown.querySelector(".dropdown-menu");
    languages.forEach(language => {
        const option = document.createElement("li");
        option.classList.add("option");
        option.dataset.value = language.code;
        option.textContent = language.name;
        dropdownMenu.appendChild(option);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    // Set the placeholder text in its original case
    var placeholderText = "Enter Latin Script text here...";
    document.getElementById("input-text").setAttribute("placeholder", placeholderText);
});

document.addEventListener("DOMContentLoaded", function () {
    var baybayinKeyboard = document.querySelector('.card-baybayin-keyboard');
    var toggleButton = document.getElementById('keyboard-display');

    // Add click event listener to the toggle button
    if (toggleButton) {
        toggleButton.addEventListener('click', function () {
            // Toggle the visibility of the keyboard by adding/removing the 'visible' class
            baybayinKeyboard.classList.toggle('visible');
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {

    const transliterateButton = document.getElementById("transliterate-button");
    const inputText = document.getElementById("input-text");
    const outputText = document.getElementById("output-text");

    transliterateButton.addEventListener("click", () => {
        const inputLangDropdown = document.getElementById("input-script");
        const outputLangDropdown = document.getElementById("output-script");

        const inputSelectedValue = inputLangDropdown.querySelector(".selected-script").dataset.value;
        const outputSelectedValue = outputLangDropdown.querySelector(".selected-script").dataset.value;

        const isLatinToBaybayin = (inputSelectedValue === "lat" && outputSelectedValue === "byn");
        const isBaybayinToLatin = (inputSelectedValue === "byn" && outputSelectedValue === "lat");

        if (isLatinToBaybayin || isBaybayinToLatin) {
            const apiEndpoint = isLatinToBaybayin ? '/api/transliterate/latin-to-baybayin' : '/api/transliterate/baybayin-to-latin';

            let requestData;
            if (isLatinToBaybayin) {
                // For Latin to Baybayin, send the entire input from the textarea
                requestData = { input: inputText.value };
            } else if (isBaybayinToLatin) {
                requestData = {
                    charInput: storedBaybayinChars.join('')
                };
            }

            fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            })
                .then(response => response.json())
                .then(data => {
                    outputText.value = data.result;

                    // Handle styling based on the result
                    if (outputText.value === "Input not available in Baybayin" && isBaybayinToLatin) {
                        outputText.style.fontFamily = "Baybayin";
                        outputText.style.fontSize = "40px";
                        inputText.style.fontFamily = "";
                        inputText.style.fontSize = "";
                    } else {
                        outputText.style.color = "";
                        outputText.style.fontFamily = isLatinToBaybayin ? "Baybayin" : "";
                    }
                })
                .catch(error => console.error('Error:', error));
        } else {
            console.error('Invalid conversion selected');
        }

    });
});

function copyToClipboard() {
    const outputTextElement = document.getElementById('output-text');

    // Create a Range object to select the text content and style
    const range = document.createRange();
    range.selectNode(outputTextElement);

    // Clear any existing selection
    window.getSelection().removeAllRanges();

    // Add the new Range to the selection
    window.getSelection().addRange(range);

    // Copy the selection to the clipboard
    document.execCommand('copy');

    // Remove the Range from the selection
    window.getSelection().removeAllRanges();
}


document.addEventListener('DOMContentLoaded', function () {
    var rulesMenu = document.querySelector('.rules-menu');
    var rulesContent = document.querySelector('.rules-content');

    rulesMenu.addEventListener('click', function () {
        var isDisplayed = window.getComputedStyle(rulesContent).display !== 'none';
        rulesContent.style.display = isDisplayed ? 'none' : 'block';
    });
});