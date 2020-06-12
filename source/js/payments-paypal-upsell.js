import initPaypal from "./components/paypal";

function setupBraintree() {
  var paymentForm = document.getElementById("payments__braintree-form"),
    nonceInput = document.getElementById("id_braintree_nonce"),
    amountInput = document.getElementById("id_amount"),
    currencyInput = document.getElementById("id_currency");

  var getAmount = () => {
    return amountInput.value;
  };
  var getCurrency = () => currencyInput.value;
  var onAuthorize = (payload) => {
    nonceInput.value = payload.nonce;
    amountInput.value = getAmount();
    paymentForm.submit();
  };

  initPaypal(
    getAmount,
    getCurrency,
    onAuthorize,
    "vault",
    "#payments__paypal-button--upsell"
  );
}

document.addEventListener("DOMContentLoaded", function () {
  setupBraintree();
});
