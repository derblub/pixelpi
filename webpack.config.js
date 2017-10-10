'use strict';

const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
// const CleanWebpackPlugin = require('clean-webpack-plugin');


console.log('env', process.env.NODE_ENV);
const debug = process.env.NODE_ENV !== "production";

const config = {
    entry: ['./static/js/main.js', './static/sass/style.scss'],
    output: {
        filename: './static/js/[name].min.js'
    },
    devtool: debug ? "inline-sourcemap" : false,
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract(['css-loader', 'sass-loader'])
            },
            {
                test: /\.js$/,
                use: 'babel-loader',
                exclude: /node_modules/
            }
        ]
    }
};

config.plugins = [
    // new CleanWebpackPlugin(['dist'])
    new webpack.ProvidePlugin({
        $: "jquery",
        jQuery: "jquery"
    }),
    new ExtractTextPlugin({ // define where to save the file
        filename: './static/css/style.css',
        allChunks: true
    })
];


if (!debug) {
    config.plugins.push(
        new webpack.optimize.UglifyJsPlugin({
            mangle: false,
            sourcemap: false,
            comments: false,
            test: /\.js$/
        })
    );
}


module.exports = config;
