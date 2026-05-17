import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface RegisterPayload {
  username: string;
  password: string;
}

interface LoginPayload {
  username: string;
  password: string;
}

interface RegisterResponse {
  id: number;
  username: string;
}

interface TokenResponse {
  access: string;
  refresh: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly apiUrl = 'http://127.0.0.1:8000/api/v1';

  constructor(private readonly http: HttpClient) {}

  register(payload: RegisterPayload): Observable<RegisterResponse> {
    return this.http.post<RegisterResponse>(
      `${this.apiUrl}/auth/register/`,
      payload,
    );
  }

  login(payload: LoginPayload): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(
      `${this.apiUrl}/auth/token/`,
      payload,
    );
  }

  saveTokens(tokens: TokenResponse): void {
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  isAuthenticated(): boolean {
    return Boolean(this.getAccessToken());
  }
}