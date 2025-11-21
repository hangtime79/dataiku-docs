/*
 * For more information, refer to the "Javascript API" documentation:
 * https://doc.dataiku.com/dss/latest/api/js/index.html
 */

let buildButton = document.getElementById('build-button');
let identifiedUser = document.getElementById('identified_user')

buildButton.addEventListener('click', function (event) {
    datasetToBuild = "web_history_prepared"
    $.get(getWebAppBackendUrl("/build_dataset"), {datasetToBuild: datasetToBuild});
});

// When loading, get the user information
$.getJSON(getWebAppBackendUrl('/get_user_name'), function (data) {
    identifiedUser.textContent = data;
});
