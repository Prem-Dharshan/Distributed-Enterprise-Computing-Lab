import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  MessageBody,
  ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';

@WebSocketGateway({ cors: { origin: '*' } })
export class DrawingGateway {
  @WebSocketServer()
  server: Server;

  // Broadcast drawing data to all clients except sender
  @SubscribeMessage('drawing')
  handleDrawing(
    @MessageBody()
    data: { x: number; y: number; prevX: number; prevY: number; color: string },
    @ConnectedSocket() client: Socket,
  ): void {
    client.broadcast.emit('drawing', data);
  }

  handleConnection(client: Socket) {
    console.log(`Client connected: ${client.id}`);
  }

  handleDisconnect(client: Socket) {
    console.log(`Client disconnected: ${client.id}`);
  }
}
