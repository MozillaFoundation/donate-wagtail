let webpack = require(`webpack`);
let path = require(`path`);
let frontendPath = path.resolve(__dirname, `donate`, `frontend`, `_js`);

let rules = [
  {
    test: /\.js(x?)$/,
    exclude: /node_modules/,
    loader: `babel-loader`,
    query: {
      presets: [[`@babel/preset-env`, { targets: `> 1%, last 2 versions` }]],
    },
  },
];

function generate(name) {
  return {
    entry: `./source/js/${name}.js`,
    output: {
      path: frontendPath,
      filename: `${name}.compiled.js`,
    },
    module: {
      rules,
    },
    devtool: `none`, // see https://webpack.js.org/configuration/devtool/
  };
}

let configs = [
  `main`,
  `payments-card`,
  `payments-paypal`,
  `payments-paypal-upsell`,
];

module.exports = configs.map((name) => generate(name));
