/**
 * Get the data from the UI, send them to the backend, and display the result on the frontend.
 * @param event: not used. Only for preventing default behavior.
 */
window.score = function (event) {
    event.preventDefault();
    let result_object = $('#result')
    result_object.text("Waiting for the result.")
    let param;
    try {
        param = makeRequestParam();
    } catch {
        result_object.text("Your data seems to be malformed.");
        return;
    }
    let url = getWebAppBackendUrl('/score');
    fetch(url, param)
        .then(response => response.text())
        .then(data => {
            let result = JSON.parse(data).result;
            if (typeof result === 'string' || result instanceof String) {
                result_object.text(result);
            } else {
                result_object.text(result.prediction);
            }
        })
        .catch(err => result_object.text(err))
}

/**
 * Create a javascript object to be sent to the server with a POST request.
 *
 * @returns {{headers: {"Content-Type": string}, method: string, body: string}}
 */
function makeRequestParam() {
    let data = {
        "url": $('#endpoint_url').val(),
        "endpoint": $('#endpoint_name').val(),
        "features": JSON.parse($('#features').val())
    }
    return {
        "method": 'POST', "headers": {
            'Content-Type': 'application/json',
        }, "body": JSON.stringify(data)
    }
}