var r = require("crypto-js")

function md5(text) {
    return r.MD5(text).toString();
}

function l(e) {
    for (var n = [], t = Array.of("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"), a = 0; a < e; a++) {
        var c = Math.floor(10 * Math.random());
        n[a] = t[c]
    }
    return n.join("")
}

function s() {
    return parseInt((new Date).getTime() / 1e3)
}



function get_par(page) {
    var headers = {}

    
    headers.data = {
        "pageNo":page,
        "pageSize":12,
        "condition":{"nodeId":436}
    }

    var n = l(10)
        , t = s() 
        , a = r.MD5(JSON.stringify(headers.data ? headers.data : "")).toString(r.enc.Hex)
        , c = ""
        , o = "0/56f5cff3cad14853a44782c2c689ab2a"
        , i = "13ade1de1eff43ffb821735f352a4148";
    headers["x-user"] = o,
    headers["x-nonce"] = n,
    headers["x-date"] = t,
    headers["Content-Md5"] = a,
    c = "".concat('POST', "\n").concat('/v1/web/api/content/list?domainId=12', "\nx-user:").concat(o, "\nx-nonce:").concat(n, "\nx-date:").concat(t, "\nContent-Md5:").concat(a, "\n");
    var u = r.HmacSHA1(c, i).toString().toUpperCase();
    headers["x-signature"] = u

    return headers
}
