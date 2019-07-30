import initPaypal from "./components/paypal";

function setupBraintree() {
  var paymentForm = document.getElementById("payments__braintree-form"),
    nonceInput = document.getElementById("id_braintree_nonce"),
    amountInput = document.getElementById("id_amount"),
    frequencyInput = document.getElementById("id_frequency"),
    currencyInput = document.getElementById("id_currency"),
    currencySelect = document.getElementById("id_currency-switcher-currency");

  var getCurrency = () => currencySelect.value.toUpperCase();
  var getAmountSingle = () => {
    var donateForm = document.getElementById("donate-form--single");
    return donateForm.querySelector('input[name="amount"]:checked').value;
  };
  var onAuthorizeSingle = payload => {
    nonceInput.value = payload.nonce;
    amountInput.value = getAmountSingle();
    frequencyInput.value = "single";
    currencyInput.value = currencySelect.value;
    paymentForm.submit();
  };
  var getAmountMonthly = () => {
    var donateForm = document.getElementById("donate-form--monthly");
    return donateForm.querySelector('input[name="amount"]:checked').value;
  };
  var onAuthorizeMonthly = payload => {
    nonceInput.value = payload.nonce;
    amountInput.value = getAmountMonthly();
    frequencyInput.value = "monthly";
    currencyInput.value = currencySelect.value;
    paymentForm.submit();
  };

  initPaypal(
    getAmountSingle,
    getCurrency,
    onAuthorizeSingle,
    "checkout",
    "#payments__paypal-button--single"
  );
  initPaypal(
    getAmountMonthly,
    getCurrency,
    onAuthorizeMonthly,
    "vault",
    "#payments__paypal-button--monthly"
  );
}

document.addEventListener("DOMContentLoaded", function() {
  setupBraintree();
});
