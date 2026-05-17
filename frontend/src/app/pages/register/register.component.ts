import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css',
})
export class RegisterComponent {
  username = '';
  password = '';
  errorMessage = '';
  successMessage = '';

  constructor(
    private readonly authService: AuthService,
    private readonly router: Router,
  ) {}

  onSubmit(): void {
    this.errorMessage = '';
    this.successMessage = '';

    this.authService.register({
      username: this.username,
      password: this.password,
    }).subscribe({
      next: () => {
        this.successMessage = 'Пользователь успешно зарегистрирован.';
        this.router.navigate(['/login']);
      },
      error: (error) => {
        this.errorMessage = 'Не удалось зарегистрироваться.';
        console.error(error);
      },
    });
  }
}
