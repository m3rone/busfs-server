// helo
function uploadFile(){
    let filein = document.getElementById("uploadfile")
    let file = null
    let description = null

    if ((file = filein.files[0]) == null) {
        return
    }
    if (document.getElementById("descriptionbox").value !== null){
        description = document.getElementById("descriptionbox").value
    } else {
        description = ""
    }

    let formData = new FormData();
    formData.append('file', file)
    formData.append('data', JSON.stringify({desc: description}))
    $.ajax({
        url: '/upload-file',
        method: 'POST',
        data: formData,
        contentType: false,
        processData: false,
    });
}