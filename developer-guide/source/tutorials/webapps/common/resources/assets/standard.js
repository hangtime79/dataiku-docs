let getImageFromManageFolderA    = document.getElementById('getImageFromManageFolderA')
let getImageFromManageFolderImg  = document.getElementById('getImageFromManageFolderImg')
let getImageFromManageFolderAImg = document.getElementById('getImageFromManageFolderAImg')
let getPDFFromManagedFolder      = document.getElementById('getPDFFromManagedFolder')
let getPDFFromManagedFolderA     = document.getElementById('getPDFFromManagedFolderA')
let getCSSFromManagedFolder      = document.getElementById('getCSSFromManagedFolder')

let getImageFromProjectLibImg    = document.getElementById('getImageFromProjectLibImg')
let getImageFromProjectLibA      = document.getElementById('getImageFromProjectLibA')
let getImageFromProjectLibAImg   = document.getElementById('getImageFromProjectLibAImg')
let getPDFFromProjectLibA        = document.getElementById('getPDFFromProjectLibA')
let getCSSFromProjectLib         = document.getElementById('getCSSFromProjectLib')

// Dynamic setting of the various element
getCSSFromManagedFolder.href     = getWebAppBackendUrl('/get_css_from_managed_folder')
getImageFromManageFolderA.href   = getWebAppBackendUrl('/get_image_from_managed_folder')
getImageFromManageFolderImg.src  = getWebAppBackendUrl('/get_image_from_managed_folder')
getImageFromManageFolderAImg.src = getWebAppBackendUrl('/get_image_from_managed_folder')
getPDFFromManagedFolderA.href    = getWebAppBackendUrl('/get_pdf_from_managed_folder')

getImageFromProjectLibImg.src  = `/local/projects/${dataiku.defaultProjectKey}/resources/image.jpg`
getImageFromProjectLibA.href   = `/local/projects/${dataiku.defaultProjectKey}/resources/image.jpg`
getImageFromProjectLibAImg.src = `/local/projects/${dataiku.defaultProjectKey}/resources/image.jpg`
getPDFFromProjectLibA.href     = `/local/projects/${dataiku.defaultProjectKey}/resources/file.pdf`
getCSSFromProjectLib.href      = `/local/projects/${dataiku.defaultProjectKey}/resources/my-css.css`


//
getPDFFromManagedFolder.addEventListener('click', () => {
    getWebAppBackendUrl('/get_pdf_from_managed_folder')
});

/* Javascript function for external URL */
let externalImageJs = document.getElementById('externalImageJs')

fetch("https://picsum.photos/200/300")
    .then(response => response.blob())
    .then(image => externalImageJs.src = URL.createObjectURL(image))