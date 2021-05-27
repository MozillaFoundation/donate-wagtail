// Importing JSON list of countries and post-code info.
// This info is also shared with donate/forms.py to check on the backend.
import countriesAndPostCodes from "./post-codes-list.json";

function enableCountryPostCodeValidation() {
  const countrySelector = document.getElementById("id_country");

  if (countrySelector && countriesAndPostCodes) {
    const postCodeInput = document.querySelector(".post-code-input");
    const formAndCityContainer = document.querySelector(
      ".form__group--city-post"
    );

    // runs once as part of our initialisation:
    checkForCountryPostCode(
      countrySelector,
      postCodeInput,
      formAndCityContainer
    );

    // add make sure this also runs every time the country selector gets changed:
    countrySelector.addEventListener("change", (e) => {
      checkForCountryPostCode(
        countrySelector,
        postCodeInput,
        formAndCityContainer
      );
    });
  }
}

function checkForCountryPostCode(
  countrySelector,
  postCodeInput,
  formAndCityContainer
) {
  const { options, selectedIndex } = countrySelector;
  const selectedCountryName = options[selectedIndex].text;

  // Finding the country object in the reference array.
  const countryObject = countriesAndPostCodes.find(
    (country) => country.name === selectedCountryName
  );

  if (countryObject !== undefined) {
    if (countryObject.postal) {
      // Display post code field.
      formAndCityContainer.style.setProperty(
        "grid-template-columns",
        "0.3fr 0.7fr"
      );
      postCodeInput.classList.remove("hidden");
    }
    // Hide post code field.
    else {
      formAndCityContainer.style.setProperty("grid-template-columns", "auto");
      postCodeInput.classList.add("hidden");
    }
  }
}

export default enableCountryPostCodeValidation;
