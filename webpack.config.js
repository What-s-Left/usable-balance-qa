const path = require('path');

module.exports = {
    entry: './app/assets/js/app.js',
    output: {
        filename: 'app.bundle.js',
        path: path.resolve(__dirname, './app/assets/js')
    },
    devtool: 'source-map'
};