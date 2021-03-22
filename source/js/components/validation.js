// Handler for "other amount" input
function otherAmountInputValidation() {
  const otherAmountInput = document.querySelector(
    ".one-time-amount-other-input"
  );
  const otherAmountErrorMessage = document.querySelector(".error-message");
  otherAmountInput.addEventListener("blur", (e) => {
    if (!document.querySelector(".donation-amount__radio:checked").length) {
      const attemptedValue = otherAmountInput.value;
      const number = Number(attemptedValue);
      if (!isNaN(number) && number) {
        // hide error message
        otherAmountErrorMessage.classList.add("hidden");
      } else {
        // display error message
        otherAmountErrorMessage.classList.remove("hidden");
      }
    }
  });
}

export default otherAmountInputValidation;
