const path = require('path')
const { VueLoaderPlugin } = require('vue-loader')
const htmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
    mode: 'development',
    entry: './src/main.js',
    output: {
        path: path.resolve(__dirname, 'dist'),
    },
    devServer: {
        static: { directory: path.join(__dirname, 'dist') },
        port: 8080,
        hot: true,
        open: true,
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    { loader: 'vue-style-loader' },
                    { loader: 'css-loader' },
                    { loader: 'sass-loader'}
                ],
            },
            {
                test: /\.vue$/i,
                exclude: /(node_modules)/,
                use: { loader: 'vue-loader' }
            },
            {
                test: /\.(js | jsx)$/,
                exclude: /(node_modules)/,
                use: { loader: 'babel-loader', options: { presets: ['@babel/preset-env'] } }
            },
            {   test: /\.html$/i,
                use: { loader: 'html-loader' }
            },
            {
                test: /\.(ts | tsx)$/,
                exclude: /(node_modules)/,
                use: { loader: 'ts-loader' }
            },
        ]
                

    },
    plugins: [
        new VueLoaderPlugin(),
        new htmlWebpackPlugin({
            template: './src/index.html',
        }),
    ]

}