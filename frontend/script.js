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

  let sio = io('ws://localhost:8000', {
        path: '/ws/socket.io'
  });


  sio.on('connect', () => {
      console.log('connected');
  });

  sio.on('download_file_progress', (data) => {
    console.log(1);
  });

  let fileInput =  document.getElementById("fileUploadInput");
  file_size = fileInput.files[0].size // Size in bytes

  fetch(`${form.action}${file_size}`, {method:'post', body: new FormData(form)});
  
  // sio.emit('download_file', '');

  e.preventDefault();
}
