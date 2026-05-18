import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Cat {
  id: number;
  name: string;
  age: number;
  breed: string;
  fluffiness: number;
  created_at: string;
  updated_at: string;
}

export interface CatPayload {
  name: string;
  age: number;
  breed: string;
  fluffiness: number;
}

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({
  providedIn: 'root',
})
export class CatService {
  private readonly apiUrl = 'http://127.0.0.1:8000/api/v1';

  constructor(private readonly http: HttpClient) {}

  getCats(): Observable<PaginatedResponse<Cat>> {
    return this.http.get<PaginatedResponse<Cat>>(
      `${this.apiUrl}/cats/`,
    );
  }

  createCat(payload: CatPayload): Observable<Cat> {
    return this.http.post<Cat>(
      `${this.apiUrl}/cats/`,
      payload,
    );
  }

  updateCat(id: number, payload: Partial<CatPayload>): Observable<Cat> {
    return this.http.patch<Cat>(
      `${this.apiUrl}/cats/${id}/`,
      payload,
    );
  }

  deleteCat(id: number): Observable<void> {
    return this.http.delete<void>(
      `${this.apiUrl}/cats/${id}/`,
    );
  }
}
