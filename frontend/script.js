// sends the entered url to the server
const sendUrl = async (e) => {

  const { value } = document.querySelector('#fileLinkInput');
  
  api_url = `http://127.0.0.1:8000/download_file?url=${value}`
  
  let response = await fetch(api_url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json;',
          'Access-Control-Allow-Origin': '*',
      },
  });   
}


// sends the file and its size to the server
function fileUpload(e, form) {

  let fileInput =  document.getElementById("fileUploadInput");
  file_size = fileInput.files[0].size // Size in bytes

  fetch(`${form.action}${file_size}`, {method:'post', body: new FormData(form)});

  e.preventDefault();
}
