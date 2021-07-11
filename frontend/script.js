// sends the entered url to the server
const sendUrl = async (e) => {

  const {value} = document.querySelector('#fileLinkInput');
  
  api_url = `http://127.0.0.1:8000/download_file`
  
  let response = await fetch(api_url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json;',
          'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({
        "url": value
      }),
  });
}


// sends the file and its size to the server
async function fileUpload(e, form) {

  let fileInput =  document.getElementById("fileUploadInput");
  file_size = fileInput.files[0].size // Size in bytes

  // let ws = new WebSocket("ws://localhost:8000/ws");

  fetch(`${form.action}${file_size}`, {method:'post', body: new FormData(form)});

  // ws.onmessage = function(event) {
  //     let messages = document.getElementById('fileUploadDiv')
  //     let message = document.createElement('div')
  //     let content = document.createTextNode(event.data)
  //     message.appendChild(content)
  //     messages.appendChild(message)
  // };

  e.preventDefault();
}
