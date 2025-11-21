$('#uploadButton').click(function (e) {
    e.preventDefault();
    let newFile = $('#newFile')[0].files[0];
    let form = new FormData();
    form.append('file', newFile);
    form.append('extra', $('#someParam').val())
    $.ajax({
        type: 'post',
        url: getWebAppBackendUrl('/upload-to-dss'),
        processData: false,
        contentType: false,
        data: form,
        success: function (data) { console.log(data); },
        error: function (jqXHR, status, errorThrown) { console.error(jqXHR.responseText); },
        xhr: function() {
            startUpload();
            var ret = new window.XMLHttpRequest();
            ret.upload.addEventListener("progress", function(evt) {
                if (evt.lengthComputable) {
                    var pct = parseInt(evt.loaded / evt.total * 100);
                    $('#progress').css("width", "" + pct + "%");
                }
            }, false);
            return ret;
        },
        complete: function() { stopUpload();}
    });
});

$('#newFile').on('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
});
$('#newFile').on('dragenter', function(e) {
    e.preventDefault();
    e.stopPropagation();
    $("#newFile").css("opacity", "0.5")
});
$('#fileGroup').on('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    $("#newFile").css("opacity", "")
});
$('#newFile').on('drop', function(e){
    $("#newFile").css("opacity", "")
    if(e.originalEvent.dataTransfer && e.originalEvent.dataTransfer.files.length) {
        e.preventDefault();
        e.stopPropagation();
        $("#newFile")[0].files = e.originalEvent.dataTransfer.files;
    }
});

let stopUpload = function() {
    $("#progress").remove();
};

let startUpload = function() {
    stopUpload();
        let progress = $('<div id="progress"/>').css("height", "10px").css("margin", "10px 0").css("background","lightblue");
    $('#fileGroup').append(progress);
};

