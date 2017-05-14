const path = require('path');

module.exports = {
    entry: './src/js/script.js',
    output: {
        path: path.resolve(__dirname, 'src/dist'),
        filename: 'madlib.bundle.js'
    }
};
