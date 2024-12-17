import React, { useEffect, useRef, useState } from 'react';
import { io, Socket } from 'socket.io-client';

const socket: Socket = io('http://localhost:3000');

function App() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const ctxRef = useRef<CanvasRenderingContext2D | null>(null);
  const isDrawingRef = useRef<boolean>(false);
  const [logs, setLogs] = useState<string[]>([]);
  const color = 'black';

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      canvas.width = window.innerWidth * 0.7 - 40;
      canvas.height = window.innerHeight - 40;
      ctxRef.current = canvas.getContext('2d');
    }

    // Listen for incoming drawing data
    socket.on('drawing', ({ x, y, prevX, prevY, color }) => {
      if (ctxRef.current) {
        drawLine(prevX, prevY, x, y, color);
      }
      setLogs((prevLogs) => [...prevLogs, `Drawing from ${prevX},${prevY} to ${x},${y}`]);
    });

    return () => {
      socket.off('drawing');
    };
  }, []);

  const drawLine = (prevX: number, prevY: number, x: number, y: number, color: string) => {
    if (ctxRef.current) {
      ctxRef.current.beginPath();
      ctxRef.current.strokeStyle = color;
      ctxRef.current.lineWidth = 3;
      ctxRef.current.moveTo(prevX, prevY);
      ctxRef.current.lineTo(x, y);
      ctxRef.current.stroke();
      ctxRef.current.closePath();
    }
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    isDrawingRef.current = true;
    const canvas = canvasRef.current;
    if (canvas) {
      const rect = canvas.getBoundingClientRect();
      canvas.dataset.prevX = String(e.clientX - rect.left);
      canvas.dataset.prevY = String(e.clientY - rect.top);
    }
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDrawingRef.current) return;

    const canvas = canvasRef.current;
    if (canvas) {
      const rect = canvas.getBoundingClientRect();
      const prevX = Number(canvas.dataset.prevX);
      const prevY = Number(canvas.dataset.prevY);
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      drawLine(prevX, prevY, x, y, color);

      // Send drawing data to the server
      socket.emit('drawing', { x, y, prevX, prevY, color });
      setLogs((prevLogs) => [...prevLogs, `You drew from ${prevX},${prevY} to ${x},${y}`]);

      canvas.dataset.prevX = String(x);
      canvas.dataset.prevY = String(y);
    }
  };

  const handleMouseUp = () => {
    isDrawingRef.current = false;
  };

  return (
      <div style={{ display: 'flex', height: '100vh', boxSizing: 'border-box', padding: '20px' }}>
        {/* Canvas on the left */}
        <div style={{ flex: 7, padding: '10px', boxSizing: 'border-box' }}>
          <h2>Collaborative Drawing Canvas</h2>
          <canvas
              ref={canvasRef}
              style={{
                border: '2px solid #000',
                display: 'block',
                cursor: 'crosshair',
                backgroundColor: '#f9f9f9',
              }}
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              onMouseOut={handleMouseUp}
          />
        </div>

        <div
            style={{
              flex: 3,
              padding: '10px',
              boxSizing: 'border-box',
              borderLeft: '2px solid #ddd',
              overflowY: 'auto',
              backgroundColor: '#f5f5f5',
            }}
        >
          <h2>Drawing Logs</h2>
          <div style={{ maxHeight: '100%', overflowY: 'auto' }}>
            {logs.map((log, index) => (
                <div key={index} style={{ marginBottom: '10px', fontSize: '14px' }}>
                  {log}
                </div>
            ))}
          </div>
        </div>
      </div>
  );
}

export default App;
