let func_name = "_ZN5Botan11PK_Verifier14verify_messageEPKhjS2_j" // 32 bit

let url_regexes = "{{URL_REGEXES}}"
let server_url = "{{URL}}"

if (is_64_bit()) {
    func_name = "_ZN5Botan11PK_Verifier14verify_messageEPKhmS2_m" // 64 bit
}

// Botan::PK_Verifier::verify_message(unsigned char const*, unsigned long, unsigned char const*, unsigned long)
Interceptor.attach(Module.findExportByName("libnative-lib.so", func_name), {
    onLeave: function (retval) {
        retval.replace(0x1)
    }
})

function does_url_match(url) {
    for (let regex in url_regexes) {
        if (url.match(url_regexes[regex])) {
            return true;
        }
    }
    return false;
}

function get_new_url(url, handle) {
    let url_obj = Java.use("java.net.URL").$new(url);

    let domain = url_obj.getHost();
    let path = url_obj.getPath();
    let query = url_obj.getQuery();
    let new_url = server_url + "/api" + path;
    if (query) {
        new_url += "?" + query;
        new_url += "&";
    }
    else {
        new_url += "?";
    }
    new_url += "req_handle=" + handle;
    new_url += "&domain=" + domain;

    let package_version = getPackageVersion();
    let package_name = getPackageName();

    new_url += "&package_version=" + package_version;
    new_url += "&package_name=" + package_name;

    return new_url;

}

Java.perform(function () {
    let MyActivity = Java.use("jp.co.ponos.battlecats.MyActivity");

    MyActivity["newHttpRequest"].implementation = function (method, url, timeout, headers, data, cookies, run_sync, stream) {
        let handle = this.mNextRequestHandle.value;
        if (does_url_match(url)) {
            url = get_new_url(url, handle);
            log("new url:" + url);
        }
        return this["newHttpRequest"](method, url, timeout, headers, data, cookies, run_sync, stream);
    };
})