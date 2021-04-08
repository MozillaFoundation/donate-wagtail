// constants for "Other Amount" inputs and error messages
const oneTimeOtherAmountInput = document.querySelector(
  ".one-time-amount-other-input"
);
const monthlyOtherAmountInput = document.querySelector(
  ".monthly-amount-other-input"
);
const oneTimeOtherAmountErrorMessage = document.querySelector(
  ".error-message__one-time-other-amount"
);
const monthlyOtherAmountErrorMessage = document.querySelector(
  ".error-message__monthly-other-amount"
);

// Handler for "other amount" inputs
function otherAmountInputValidation() {
  oneTimeOtherAmountInput.addEventListener("blur", (e) => {
    if (document.querySelector(".one-time-donation-amount-radio:checked")) {
      inputValueCheck(oneTimeOtherAmountInput, oneTimeOtherAmountErrorMessage);
    }
  });
  monthlyOtherAmountInput.addEventListener("blur", (e) => {
    if (document.querySelector(".monthly-donation-amount-radio:checked")) {
      inputValueCheck(monthlyOtherAmountInput, monthlyOtherAmountErrorMessage);
    }
  });
}

function inputValueCheck(inputObjectToValidate, messageToUpdate) {
  const number = parseFloat(inputObjectToValidate.value);
  const minimumAmount = parseFloat(inputObjectToValidate.min);
  const maximumAmount = parseFloat(inputObjectToValidate.max);
  // We are getting the minimum and maximum amount for input above as these can change based on currency
  if (
    !isNaN(number) &&
    number &&
    number >= minimumAmount &&
    number <= maximumAmount
  ) {
    // hide error message
    messageToUpdate.classList.add("hidden");
  } else {
    // display error message
    messageToUpdate.classList.remove("hidden");
  }
}

export default otherAmountInputValidation;
