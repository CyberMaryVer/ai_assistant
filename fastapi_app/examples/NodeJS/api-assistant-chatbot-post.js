const axios = require('axios');

const userId = '123'; // Replace with actual user ID
const endpointUrl = 'https://{your_company}.com/api/assistant/chatbot/${userId}';

const payload = {
  user_input: 'string',
};

axios.post(endpointUrl, payload)
  .then((response) => {
    console.log('Response:', response.data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });