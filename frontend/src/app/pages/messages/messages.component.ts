import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';

import {
  Message,
  MessageService,
} from '../../core/services/message.service';
import {
  WebSocketMessage,
  WebSocketService,
} from '../../core/services/websocket.service';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-messages',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './messages.component.html',
  styleUrl: './messages.component.css',
})
export class MessagesComponent implements OnInit, OnDestroy {
  messages: WebSocketMessage[] = [];

  receiverId: number | null = null;
  text = '';

  errorMessage = '';
  successMessage = '';

  private subscription: Subscription | null = null;

  constructor(
    private readonly messageService: MessageService,
    private readonly websocketService: WebSocketService,
    private readonly authService: AuthService,
  ) {}

  ngOnInit(): void {
    this.loadMessages();
    this.connectWebSocket();
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
    this.websocketService.disconnect();
  }

  loadMessages(): void {
    this.messageService.getMessages().subscribe({
      next: (response) => {
        this.messages = response.results.map((message: Message) => ({
          id: message.id,
          sender_id: message.sender,
          sender_username: message.sender_username,
          receiver_id: message.receiver,
          text: message.text,
          created_at: message.created_at,
        }));
      },
      error: (error) => {
        this.errorMessage = 'Не удалось загрузить историю сообщений.';
        console.error(error);
      },
    });
  }

  connectWebSocket(): void {
    const accessToken = this.authService.getAccessToken();

    if (!accessToken) {
      this.errorMessage = 'Не найден access token. Войдите заново.';
      return;
    }

    this.websocketService.connect(accessToken);

    this.subscription = this.websocketService.messages$.subscribe({
      next: (data) => {
        if (data.error) {
          this.errorMessage = data.error;
          return;
        }

        if (data.status === 'sent' && data.message) {
          this.successMessage = 'Сообщение отправлено.';
          this.messages.push(data.message);
          return;
        }

        this.messages.push(data);
      },
    });
  }

  sendMessage(): void {
    this.errorMessage = '';
    this.successMessage = '';

    if (!this.receiverId) {
      this.errorMessage = 'Укажите ID получателя.';
      return;
    }

    if (!this.text.trim()) {
      this.errorMessage = 'Введите текст сообщения.';
      return;
    }

    try {
      this.websocketService.sendMessage(
        Number(this.receiverId),
        this.text.trim(),
      );
      this.text = '';
    } catch (error) {
      this.errorMessage = 'WebSocket не подключён.';
      console.error(error);
    }
  }
}
