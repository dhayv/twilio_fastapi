const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/'
})

document.getElementById('formData').addEventListener('submit', function (event) {
  event.preventDefault()

  const inputValue = document.getElementById('userInput').value.trim()

  const data = { message: inputValue }

  // send user question
  api.post('/usersearch', data)
    .then((response) => {
      console.log(response.data)
      const requestId = response.data.requestId

      // retreive ai response
      return api.get('/response', { params: { requestId } })
    })

    .then((response) => {
      console.log(response.data)
      const responseInput = document.getElementById('responseInput')
      responseInput.value = response.data.response
      adjustTexareaHeight(responseInput)
    })
    .catch((error) => {
      console.log(error)
    })
})

const userInput = document.getElementById('userInput')
const hiddenSpan = document.getElementById('hiddenSpan')

userInput.addEventListener('input', function () {
  hiddenSpan.textContent = userInput.value
  adjustTexareaHeight(userInput)
})

function adjustTexareaHeight (textarea) {
  textarea.style.height = 'auto' // Reset the height
  textarea.style.height = (textarea.scrollHeight + 2) + 'px' // Adjust based on scroll height
}

const responseInput = document.getElementById('responseInput')
adjustTexareaHeight(responseInput)
