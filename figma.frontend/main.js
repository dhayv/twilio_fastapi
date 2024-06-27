import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000' 
});


document.getElementById("formData").addEventListener('submit', function(event){
    event.preventDefault();


    const inputValue = document.getElementById("userInput").value;

    const data = { input: inputValue}

    api.post("", data)

});