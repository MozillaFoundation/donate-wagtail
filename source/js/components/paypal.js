import client from "braintree-web/client";
import { create as paypalCreate } from "braintree-web/paypal-checkout";
import gaEvent from "./analytics";

export default function initPaypal(
  getAmount,
  getCurrency,
  onAuthorize,
  flow,
  buttonId
) {
  var loadingErrorMsg = window.gettext(
    "An error occurred. Please reload the page or try again later."
  );
  var generalErrorMsg = window.gettext(
    "There was an error processing your payment. Please try again."
  );
  var braintreeParams = JSON.parse(
    document.getElementById("payments__braintree-params").textContent
  );
  var errorDiv = document.getElementById("payments__braintree-errors-paypal");

  var showErrorMessage = msg => {
    errorDiv.toggleAttribute("hidden", false);
    errorDiv.innerHTML = msg;
  };

  var clearErrorMessage = () => {
    errorDiv.toggleAttribute("hidden", true);
    errorDiv.innerHTML = "";
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
            size: "responsive",
            color: "blue",
            shape: "rect",
            label: "paypal",
            tagline: "false"
          },

          payment: function() {
            return paypalCheckoutInstance.createPayment({
              flow: flow,
              amount: getAmount(),
              currency: getCurrency(),
              enableShippingAddress: false
            });
          },

          onAuthorize: function(data) {
            return paypalCheckoutInstance.tokenizePayment(data, function(
              err,
              payload
            ) {
              if (err) {
                showErrorMessage(generalErrorMsg);
                return;
              }

              onAuthorize(payload);
            });
          },

          onCancel: function() {
            showErrorMessage(window.gettext("Payment cancelled"));
            gaEvent({
              eventCategory: "User Flow",
              eventAction: "Paypal Payment Cancelled"
            });
          },

          onError: function(err) {
            showErrorMessage(generalErrorMsg);
            gaEvent({
              eventCategory: "User Flow",
              eventAction: "PayPal Error"
            });
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
