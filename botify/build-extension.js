const fs = require('fs');
const path = require('path');

function postBuild() {
    const buildPath = path.join(__dirname, 'build');
    const publicPath = path.join(__dirname, 'public');
    
    const jsPath = path.join(buildPath, 'static', 'js');
    const jsFiles = fs.readdirSync(jsPath);
    const mainJsFile = jsFiles.find(f => f.startsWith('main.') && f.endsWith('.js'));
    if (mainJsFile) {
        fs.copyFileSync(
            path.join(jsPath, mainJsFile),
            path.join(buildPath, 'static', 'js', 'main.js')
        );
    }
    const cssPath = path.join(buildPath, 'static', 'css');
    const cssFiles = fs.readdirSync(cssPath);
    const mainCssFile = cssFiles.find(f => f.startsWith('main.') && f.endsWith('.css'));
    if (mainCssFile) {
        fs.copyFileSync(
            path.join(cssPath, mainCssFile),
            path.join(buildPath, 'static', 'css', 'main.css')
        );
    }
}

postBuild();