let path = require(`path`);
let frontendPath = path.resolve(__dirname, `donate`, `frontend`, `_js`);

let rules = [
  {
    test: /\.js(x?)$/,
    exclude: /node_modules/,
    loader: `babel-loader`,
    query: {
      presets: [
        [`@babel/preset-env`, { targets: `> 1%, last 2 versions` }],
        [`@babel/preset-react`]
      ]
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

let payments = {
  entry: `./source/js/payments.js`,
  output: {
    path: frontendPath,
    filename: `payments.compiled.js`
  },
  module: {
    rules
  }
};

module.exports = [main, payments];
