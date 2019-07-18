import client from "braintree-web/client";
import { create as paypalCreate } from "braintree-web/paypal-checkout";

function setupBraintree() {
  var paymentForm = document.getElementById("payments__braintree-form"),
    nonceInput = document.getElementById("id_braintree_nonce"),
    submitButton = document.getElementById("payments__payment-submit"),
    token = paymentForm.getAttribute("data-token"),
    loadingErrorMsg =
      "An error occurred. Please reload the page or try again later.",
    paymentAmount = paymentForm.getAttribute("data-amount"),
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

  function showFieldError(container) {
    container.classList.add(braintreeErrorClass);
  }

  function clearFieldError(container) {
    container.classList.remove(braintreeErrorClass);
  }

  function initPaypal() {
    client.create({ authorization: token }, function(
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

            payment: function() {
              return paypalCheckoutInstance.createPayment({
                flow: braintreeParams.flow,
                amount: paymentAmount,
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
                paymentForm.submit();
              });
            },

            onCancel: function() {
              showErrorMessage("Payment cancelled");
            },

            onError: function() {
              showErrorMessage(
                "There was an error processing your payment. Please try again."
              );
            }
          },
          "#payments__paypal-button"
        ).then(function() {
          // The PayPal button will be rendered in an html element with the id
          // `paypal-button`. This function will be called when the PayPal button
          // is set up and ready to be used.
        });
      });
    });
  }

  initPaypal();
}

document.addEventListener("DOMContentLoaded", function() {
  setupBraintree();
});
