const { override, addWebpackPlugin } = require('customize-cra');
const WorkboxPlugin = require('workbox-webpack-plugin');

module.exports = override(
  addWebpackPlugin(
    new WorkboxPlugin.GenerateSW({
      clientsClaim: true,
      skipWaiting: true,
    })
  )
);
