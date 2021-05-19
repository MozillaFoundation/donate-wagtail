import { countriesAndPostCodes } from "./post-codes-list.js";

// List of countries to use for reference
const listOfCountries = countriesAndPostCodes;

// The container for the post-code input field
const postCodeInputContainer = document.querySelector(
  ".post-code-input-container"
);

// The container that houses both the post code and city inputs
const formAndCityContainer = document.querySelector(".form__group--city-post");

// The select object that allows users to select their country
const countrySelector = document.getElementById("id_country");

// Calling the function once to check in case the user refreshes the page,
// we want the input to remain one column if needed
checkForCountrysPostCode();

// Event listener for checking whether or not to display the post code field whenever the user selects a new country.
function countryPostCodeValidation() {
  countrySelector.addEventListener("change", (e) => {
    checkForCountrysPostCode();
  });
}

function checkForCountrysPostCode() {
  // The users selected country
  const selectedCountrysName =
    countrySelector.options[countrySelector.selectedIndex].text;

  // Finding the country object in the array.
  const countryObject = listOfCountries.find(
    (country) => country.name === selectedCountrysName
  );

  // If the country exists in the array, check whether or not it has a post code.
  if (countryObject !== undefined) {
    // If the country does NOT have a post code, remove the zip code field.
    if (!countryObject.hasOwnProperty("postal")) {
      formAndCityContainer.classList.add("form__group--city-post--full-width");
      postCodeInputContainer.classList.add("hidden");
    }
    // If they select a country WITH a post code, make the zip code reappear.
    else {
      formAndCityContainer.classList.remove(
        "form__group--city-post--full-width"
      );
      postCodeInputContainer.classList.remove("hidden");
    }
  }
}

export default countryPostCodeValidation;
