
function titleCase(data) {
    data = data.toLowerCase().split(' ');
    for (var i = 0; i < data.length; i++) {
      data[i] = data[i].charAt(0).toUpperCase() + data[i].slice(1); 
    }
    return data.join(' ');
  }

(async function() {

    
    let xhrResponse = await xhrRequest("get", "json", "/jabatan/daftar")

    let data = xhrResponse.response['data']

    let optionsList = '<option>Pilih</option>'


    for(let i = 0; i < data.length ; i++) {
        if(data[i]['id'] === 5077688091934720 || data[i]['id'] === 5630815723585536 ) continue
        optionsList += "<option name=jabatan value='" + data[i]['id'] +"'> " + titleCase(data[i]['nama']) + " </option>"
    }

    $('#select-jabatan').append(optionsList);

}());
