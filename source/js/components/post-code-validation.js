import { countriesAndPostCodes } from "./post-codes-list.js";

// The container for the post-code input field.
const postCodeInputContainer = document.querySelector(
  ".post-code-input-container"
);

// The container that houses both the post code and city inputs.
const formAndCityContainer = document.querySelector(".form__group--city-post");

// The select object that allows users to select their country.
const countrySelector = document.getElementById("id_country");

// If you are on the form page, check if users country uses post code.
if (countrySelector) {
  checkForCountryPostCode();
}
// Event listener for checking post-code when user selects new country.
function countryPostCodeValidation() {
  if (countrySelector) {
    countrySelector.addEventListener("change", (e) => {
      checkForCountryPostCode();
    });
  }
}

function checkForCountryPostCode() {
  // The users selected country.
  const selectedCountrysName =
    countrySelector.options[countrySelector.selectedIndex].text;

  // Finding the country object in the reference array.
  const countryObject = countriesAndPostCodes.find(
    (country) => country.name === selectedCountrysName
  );

  if (countryObject !== undefined) {
    if (countryObject.postal) {
      // Display post code field.
      formAndCityContainer.classList.remove(
        "form__group--city-post--full-width"
      );
      postCodeInputContainer.classList.remove("hidden");
    }
    // Hide post code field.
    else {
      formAndCityContainer.classList.add("form__group--city-post--full-width");
      postCodeInputContainer.classList.add("hidden");
    }
  }
}

export default countryPostCodeValidation;
