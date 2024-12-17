import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

const socket: Socket = io('http://localhost:3000'); // Connect to the server

function App() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<{ senderId: string; message: string }[]>([]);

  useEffect(() => {
    // Listen for messages from the server
    socket.on('receiveMessage', (data) => {
      setMessages((prev) => [...prev, data]);
    });

    // Cleanup on unmount
    return () => {
      socket.off('receiveMessage');
    };
  }, []);

  const sendMessage = () => {
    if (message.trim()) {
      socket.emit('sendMessage', message); // Send a message to the server
      setMessage('');
    }
  };

  return (
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
        <h1>Chat Room</h1>
        <div
            style={{
              border: '1px solid #ccc',
              padding: '10px',
              height: '300px',
              overflowY: 'auto',
              marginBottom: '10px',
            }}
        >
          {messages.map((msg, index) => (
              <div key={index} style={{ margin: '5px 0' }}>
                <strong>{msg.senderId}:</strong> {msg.message}
              </div>
          ))}
        </div>
        <div>
          <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your message..."
              style={{
                padding: '10px',
                width: '80%',
                marginRight: '10px',
                borderRadius: '5px',
                border: '1px solid #ccc',
              }}
          />
          <button
              onClick={sendMessage}
              style={{
                padding: '10px',
                borderRadius: '5px',
                border: 'none',
                backgroundColor: '#007BFF',
                color: '#fff',
                cursor: 'pointer',
              }}
          >
            Send
          </button>
        </div>
      </div>
  );
}

export default App;
