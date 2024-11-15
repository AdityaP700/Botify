// webpack.config.js
const path = require('path');
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: {
    popup: './src/index.js',
    background: './src/background/background.js'
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
    clean: true
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      }
    ]
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        { 
          from: 'public', 
          to: '',
          globOptions: {
            ignore: ['**/index.html']
          }
        },
        {
          from: 'public/index.html',
          to: 'popup.html',
          transform(content) {
            return content
              .toString()
              .replace('src/index.js', 'popup.js')
              .replace('</body>', '<script src="popup.js"></script></body>');
          },
        }
      ],
    }),
  ],
  resolve: {
    extensions: ['.js', '.jsx']
  },
};
