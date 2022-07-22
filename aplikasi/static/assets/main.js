async function xhrRequest(method, respondType, url, data){
    return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url, true);
        xhr.responseType = respondType;
        xhr.onloadend = function () {
            let status = xhr.status;
            if (status === 200) {
                resolve(xhr);
            } else {
                reject(xhr)
            }
        };
        xhr.send(data);
    }).catch((response)=>{
        // catch error and return
        return response
    })
}

async function json2fd(item){
    let fd = new FormData()
    for (let key in item ) {
    let data = item[key]
    if (typeof item[key] === "object"){
      data = JSON.stringify(item[key])
    }
        fd.append(key, data);
    }
    return fd
}

