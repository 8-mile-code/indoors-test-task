import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

export interface WebSocketMessage {
  id?: number;
  sender_id?: number;
  sender_username?: string;
  receiver_id?: number;
  text?: string;
  created_at?: string;
  status?: string;
  message?: WebSocketMessage;
  error?: string;
}

@Injectable({
  providedIn: 'root',
})
export class WebSocketService {
  private socket: WebSocket | null = null;
  private readonly messagesSubject = new Subject<WebSocketMessage>();

  messages$ = this.messagesSubject.asObservable();

  connect(accessToken: string): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      return;
    }

    this.socket = new WebSocket(
      `ws://127.0.0.1:8000/ws/chat/?token=${accessToken}`,
    );

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.messagesSubject.next(data);
    };

    this.socket.onerror = (event) => {
      console.error('WebSocket error:', event);
    };

    this.socket.onclose = () => {
      console.log('WebSocket connection closed');
    };
  }

  sendMessage(receiverId: number, text: string): void {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket is not connected.');
    }

    this.socket.send(
      JSON.stringify({
        receiver_id: receiverId,
        text,
      }),
    );
  }

  disconnect(): void {
    this.socket?.close();
    this.socket = null;
  }
}