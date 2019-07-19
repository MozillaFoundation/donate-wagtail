import client from "braintree-web/client";
import { create as paypalCreate } from "braintree-web/paypal-checkout";

function setupBraintree() {
  var paymentForm = document.getElementById("payments__braintree-form"),
    nonceInput = document.getElementById("id_braintree_nonce"),
    amountInput = document.getElementById("id_amount"),
    frequencyInput = document.getElementById("id_frequency"),
    loadingErrorMsg =
      "An error occurred. Please reload the page or try again later.",
    paymentCurrency = "USD",
    errorDiv = document.getElementById("payments__braintree-errors-paypal"),
    braintreeParams = JSON.parse(
      document.getElementById("payments__braintree-params").textContent
    );

  function showErrorMessage(msg) {
    errorDiv.toggleAttribute("hidden", false);
    errorDiv.innerHTML = msg;
  }

  function clearErrorMessage() {
    errorDiv.toggleAttribute("hidden", true);
    errorDiv.innerHTML = "";
  }

  function initPaypal(frequency, flow, buttonId) {
    var donateForm = document.getElementById("donate-form--" + frequency);
    var getAmount = function() {
      return donateForm.querySelector('input[name="amount"]:checked').value;
    };
    client.create({ authorization: braintreeParams.token }, function(
      clientErr,
      clientInstance
    ) {
      if (clientErr) {
        showErrorMessage(loadingErrorMsg);
        return;
      }

      paypalCreate({ client: clientInstance }, function(
        paypalCheckoutErr,
        paypalCheckoutInstance
      ) {
        if (paypalCheckoutErr) {
          showErrorMessage(loadingErrorMsg);
          return;
        }

        // Set up PayPal with the checkout.js library
        window.paypal.Button.render(
          {
            env: braintreeParams.use_sandbox ? "sandbox" : "production",
            commit: true,
            style: {
              size: "medium",
              color: "gold",
              shape: "pill",
              label: "paypal",
              tagline: "false"
            },

            payment: function() {
              return paypalCheckoutInstance.createPayment({
                flow: flow,
                amount: getAmount(),
                currency: paymentCurrency,
                enableShippingAddress: false
              });
            },

            onAuthorize: function(data) {
              return paypalCheckoutInstance.tokenizePayment(data, function(
                err,
                payload
              ) {
                if (err) {
                  showErrorMessage(
                    "There was an error processing your payment. Please try again."
                  );
                  return;
                }

                nonceInput.value = payload.nonce;
                amountInput.value = getAmount();
                frequencyInput.value = frequency;
                paymentForm.submit();
              });
            },

            onCancel: function() {
              showErrorMessage("Payment cancelled");
            },

            onError: function(err) {
              // TODO - we will end up here if no amount is selected, and should report
              // that meaningfully to the user.
              showErrorMessage(
                "There was an error processing your payment. Please try again."
              );
            }
          },
          buttonId
        ).then(function() {
          // The PayPal button will be rendered in an html element with the id
          // specified in buttonId. This function will be called when the PayPal button
          // is set up and ready to be used.
        });
      });
    });
  }

  initPaypal("single", "checkout", "#payments__paypal-button--single");
  initPaypal("monthly", "vault", "#payments__paypal-button--monthly");
}

document.addEventListener("DOMContentLoaded", function() {
  setupBraintree();
});
