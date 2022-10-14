// Handler for "other amount" inputs
function otherAmountInputValidation() {
  // constants for "Other Amount" inputs and error messages
  var oneTimeOtherAmountInput = document.getElementById(
      "one-time-amount-other-input"
    ),
    monthlyOtherAmountInput = document.getElementById(
      "monthly-amount-other-input"
    ),
    oneTimeOtherAmountErrorMessage = document.getElementById(
      "other-one-time-amount-error-message"
    ),
    monthlyOtherAmountErrorMessage = document.getElementById(
      "other-monthly-amount-error-message"
    );
  if (oneTimeOtherAmountInput) {
    oneTimeOtherAmountInput.addEventListener("blur", (e) => {
      if (document.querySelector(".one-time-amount-donation-radio:checked")) {
        inputValueCheck(
          oneTimeOtherAmountInput,
          oneTimeOtherAmountErrorMessage
        );
      }
    });
  }
  if (monthlyOtherAmountInput) {
    monthlyOtherAmountInput.addEventListener("blur", (e) => {
      if (document.querySelector(".monthly-amount-donation-radio:checked")) {
        inputValueCheck(
          monthlyOtherAmountInput,
          monthlyOtherAmountErrorMessage
        );
      }
    });
  }
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
