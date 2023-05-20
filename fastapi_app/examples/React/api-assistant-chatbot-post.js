import React, { useState } from 'react';

function MyComponent() {
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleButtonClick = async () => {
    const userId = '123';
    const endpointUrl = 'https://{your_company}.com/api/assistant/chatbot/${userId}';

    const payload = {
      user_input: 'string',
    };

    try {
      const response = await fetch(endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        const data = await response.json();
        setResponse(data);
        setError(null);
      } else {
        throw new Error(response.statusText);
      }
    } catch (error) {
      setResponse(null);
      setError(error.message);
    }
  };

  return (
    <div>
      <button onClick={handleButtonClick}>Make API Request</button>
      {response && <p>Response: {JSON.stringify(response)}</p>}
      {error && <p>Error: {error}</p>}
    </div>
  );
}

export default MyComponent;
