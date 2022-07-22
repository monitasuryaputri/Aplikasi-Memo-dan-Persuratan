

(async function() {
    let xhrResponse = await xhrRequest("get", "json", "/jabatan/disposisi")
    daftarJabatan = xhrResponse.response['data']

}());


function titleCase(data) {
    data = data.toLowerCase().split(' ');
    for (var i = 0; i < data.length; i++) {
      data[i] = data[i].charAt(0).toUpperCase() + data[i].slice(1); 
    }
    return data.join(' ');
  }

let room = 1;

function education_fields() {

    room++;
    var objTo = document.getElementById('education_fields')
    var divtest = document.createElement("div");
    divtest.setAttribute("class", "form-group removeclass" + room);
    var rdiv = 'removeclass' + room;
                                                        
    let optionHtml = '<div class="m-t-5">'

    optionHtml += '<select name="disposisi" class="select-jabatan form-control custom-select" style="width: 100%; height:36px;">'

    optionHtml += '<option>Pilih</option>'

    for(let i = 0; i < daftarJabatan.length ; i++) {
        optionHtml += "<option name=jabatan[] value='" + daftarJabatan[i]['id'] +"'> " + titleCase(daftarJabatan[i]['nama']) + " </option>"
    }

    optionHtml += '</select></div><div class="m-t-5"> <button class="btn btn-danger" type="button" onclick="remove_education_fields(' + room + ');"> <i class="fa fa-minus"></i> </button></div></div></div></div><div class="clear"></div></row>'

    divtest.innerHTML = optionHtml


    objTo.appendChild(divtest)
}

function remove_education_fields(rid) {
    $('.removeclass' + rid).remove();
}
