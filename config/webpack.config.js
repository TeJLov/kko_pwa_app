const WorkboxPlugin = require('workbox-webpack-plugin');

// Внутри массива plugins
new WorkboxPlugin.GenerateSW({
  clientsClaim: true,
  skipWaiting: true,
})
