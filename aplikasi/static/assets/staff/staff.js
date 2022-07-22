var daftarJabatan


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



async function konfirmasi(id_suratmasuk){

    $('#loading-btn').removeAttr('hidden');
    $('#konfirmasi-btn').attr('hidden', true);

    let listJabatan = $('.select-jabatan').find(":selected")
    
    let listNamaJabatan = []

    for (let index = 0; index < listJabatan.length; index++) {
        // if(daftarJabatan[index]['id'] === 5077688091934720 ) continue
        listNamaJabatan.push(listJabatan[index].value)        
    }

    let dataSurat = {
        'id' : id_suratmasuk,
        'penerima' : listNamaJabatan
    }


    let postData = await xhrRequest("POST", "JSON", `/staff/detailsuratmasukstaff/update/${id_suratmasuk}`, await json2fd(dataSurat))
    
    console.log(postData)
    location.reload()
    // window.location = "/kepalaupt/suratmasukka";
}


async function tugaskan(id_suratkeluar){

    $('#loading-btn').removeAttr('hidden');
    $('#konfirmasi-btn').attr('hidden', true);

    let listJabatan = $('.select-jabatan').find(":selected")
    
    let listNamaJabatan = []

    for (let index = 0; index < listJabatan.length; index++) {
        // if(daftarJabatan[index]['id'] === 5077688091934720 ) continue
        listNamaJabatan.push(listJabatan[index].value)        
    }

    let dataSurat = {
        'id' : id_suratkeluar,
        'penerima' : listNamaJabatan
    }

    let postData = await xhrRequest("POST", "JSON", `/staff/detaildrafsuratstaff/tugaskan/${id_suratkeluar}`, await json2fd(dataSurat))
    
    location.reload()
}


let room = 1;

function education_fields() {

    room++;
    var objTo = document.getElementById('education_fields')
    var divtest = document.createElement("div");
    divtest.setAttribute("class", "form-group removeclass" + room);
    var rdiv = 'removeclass' + room;
                                                        
    let optionHtml = '<div class="form-group">'

    optionHtml += '<select class="select-jabatan form-control custom-select" style="width: 100%; height:36px;">'

    optionHtml += '<option>Pilih</option>'

    for(let i = 0; i < daftarJabatan.length ; i++) {
        optionHtml += "<option name=jabatan[] value='" + daftarJabatan[i]['id'] +"'> " + titleCase(daftarJabatan[i]['nama']) + " </option>"
    }

    optionHtml += '</select></div><div class="input-group-append"> <button class="btn btn-danger" type="button" onclick="remove_education_fields(' + room + ');"> <i class="fa fa-minus"></i> </button></div></div></div></div><div class="clear"></div></row>'

    divtest.innerHTML = optionHtml


    objTo.appendChild(divtest)
}

function remove_education_fields(rid) {
    $('.removeclass' + rid).remove();
}

