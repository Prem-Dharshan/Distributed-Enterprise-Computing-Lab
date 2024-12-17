import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  MessageBody,
  ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';

@WebSocketGateway({ cors: { origin: '*' } })
export class ChatGateway {
  @WebSocketServer()
  server: Server;

  // Handle a message sent by a client
  @SubscribeMessage('sendMessage')
  handleMessage(
    @MessageBody() message: string,
    @ConnectedSocket() client: Socket,
  ): void {
    // Emit the message to all connected clients
    this.server.emit('receiveMessage', { message, senderId: client.id });
  }

  // Handle client connections
  handleConnection(client: Socket) {
    console.log(`Client connected: ${client.id}`);
    this.server.emit('receiveMessage', {
      message: `User ${client.id} has joined the chat.`,
      senderId: 'Server',
    });
  }

  // Handle client disconnections
  handleDisconnect(client: Socket) {
    console.log(`Client disconnected: ${client.id}`);
    this.server.emit('receiveMessage', {
      message: `User ${client.id} has left the chat.`,
      senderId: 'Server',
    });
  }
}
