window.send_data = function (e) {
    e.preventDefault()
    param = makeRequestParam()
    let url = getWebAppBackendUrl('/first_form')
    fetch(url, param)
        .then((response) => extractJSON(response))
        .then((json) => displayResponse(json))
        .catch((error) => console.log(error))

    return false
}

function extractJSON(response) {
    return response.json()
}

const toastLiveExample = document.getElementById('liveToast')

function displayResponse(response) {
    let message = `The server respond ${JSON.stringify(response)}`
    const toast = new bootstrap.Toast(toastLiveExample)
    $("#feedback").text(message)
    toast.show()
}

function getName() {
    return $('#name').val()
}

function makeRequestParam() {
    let data = {
        "name": getName()
    }
    return {
        "method": 'POST',
        "headers": {
            'Content-Type': 'application/json',
        },
        "body": JSON.stringify(data)
    }
}