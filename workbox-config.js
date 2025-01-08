   // workbox-config.js
   module.exports = {
    globDirectory: 'build/',
    globPatterns: [
      '**/*.{html,js,css,png,jpg,jpeg,svg,ico,json}'
    ],
    swDest: 'build/service-worker.js',
    runtimeCaching: [{
      urlPattern: /\.(?:js|css|html)$/,
      handler: 'StaleWhileRevalidate',
    }],
    modifyURLPrefix: {
      '': '/',
    },
  };