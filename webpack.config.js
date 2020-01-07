let webpack = require(`webpack`);
let path = require(`path`);
let frontendPath = path.resolve(__dirname, `donate`, `frontend`, `_js`);

let rules = [
  {
    test: /\.js(x?)$/,
    exclude: /node_modules/,
    loader: `babel-loader`,
    query: {
      presets: [[`@babel/preset-env`, { targets: `> 1%, last 2 versions` }]]
    }
  }
];

let main = {
  entry: `./source/js/main.js`,
  output: {
    path: frontendPath,
    filename: `main.compiled.js`
  },
  module: {
    rules
  }
};

let paymentsCard = {
  entry: `./source/js/payments-card.js`,
  output: {
    path: frontendPath,
    filename: `payments-card.compiled.js`
  },
  module: {
    rules
  }
};

let paymentsPaypal = {
  entry: `./source/js/payments-paypal.js`,
  output: {
    path: frontendPath,
    filename: `payments-paypal.compiled.js`
  },
  module: {
    rules
  }
};

let paymentsPaypalUpsell = {
  entry: `./source/js/payments-paypal-upsell.js`,
  output: {
    path: frontendPath,
    filename: `payments-paypal-upsell.compiled.js`
  },
  module: {
    rules
  }
};

module.exports = [main, paymentsCard, paymentsPaypal, paymentsPaypalUpsell];
