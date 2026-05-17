import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  username = '';
  password = '';
  errorMessage = '';

  constructor(
    private readonly authService: AuthService,
    private readonly router: Router,
  ) {}

  onSubmit(): void {
    this.errorMessage = '';

    this.authService.login({
      username: this.username,
      password: this.password,
    }).subscribe({
      next: (tokens) => {
        this.authService.saveTokens(tokens);
        this.router.navigate(['/cats']);
      },
      error: (error) => {
        this.errorMessage = 'Неверный username или password.';
        console.error(error);
      },
    });
  }
}