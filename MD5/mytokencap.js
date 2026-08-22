var crypto_js = require('crypto-js')


function get_params() {
    var t = Date.now().toString();
    var code = crypto_js.MD5(t + "9527" + t.substr(0, 6)).toString()
    return {
        time: t,
        code: code
    }
}

console.log(get_params());