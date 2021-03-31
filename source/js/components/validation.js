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
      const attemptedValue = oneTimeOtherAmountInput.value;
      inputValueCheck(attemptedValue, oneTimeOtherAmountErrorMessage);
    }
  });
  monthlyOtherAmountInput.addEventListener("blur", (e) => {
    if (document.querySelector(".monthly-donation-amount-radio:checked")) {
      const attemptedValue = monthlyOtherAmountInput.value;
      inputValueCheck(attemptedValue, monthlyOtherAmountErrorMessage);
    }
  });
}

function inputValueCheck(valueToCheck, messageToUpdate) {
  const number = parseFloat(valueToCheck);
  // Checking if attempted value is a number and >= 2
  if (!isNaN(number) && number && number >= 2) {
    // hide error message
    messageToUpdate.classList.add("hidden");
  } else {
    // display error message
    messageToUpdate.classList.remove("hidden");
  }
}

export default otherAmountInputValidation;
