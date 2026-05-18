import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

import {
  Cat,
  CatPayload,
  CatService,
} from '../../core/services/cat.service';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-cats',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './cats.component.html',
  styleUrl: './cats.component.css',
})
export class CatsComponent implements OnInit {
  cats: Cat[] = [];

  name = '';
  age = 1;
  breed = '';
  fluffiness = 1;

  editingCatId: number | null = null;

  errorMessage = '';
  successMessage = '';

  constructor(
    private readonly catService: CatService,
    private readonly authService: AuthService,
  ) {}

  ngOnInit(): void {
    this.loadCats();
  }

  loadCats(): void {
    this.catService.getCats().subscribe({
      next: (response) => {
        this.cats = response.results;
      },
      error: (error) => {
        this.errorMessage = 'Не удалось загрузить список котов.';
        console.error(error);
      },
    });
  }

  onSubmit(): void {
    this.errorMessage = '';
    this.successMessage = '';

    const payload: CatPayload = {
      name: this.name,
      age: Number(this.age),
      breed: this.breed,
      fluffiness: Number(this.fluffiness),
    };

    if (this.editingCatId) {
      this.catService.updateCat(this.editingCatId, payload).subscribe({
        next: () => {
          this.successMessage = 'Кот обновлён.';
          this.resetForm();
          this.loadCats();
        },
        error: (error) => {
          this.errorMessage = 'Не удалось обновить кота.';
          console.error(error);
        },
      });

      return;
    }

    this.catService.createCat(payload).subscribe({
      next: () => {
        this.successMessage = 'Кот создан.';
        this.resetForm();
        this.loadCats();
      },
      error: (error) => {
        this.errorMessage = 'Не удалось создать кота.';
        console.error(error);
      },
    });
  }

  editCat(cat: Cat): void {
    this.editingCatId = cat.id;
    this.name = cat.name;
    this.age = cat.age;
    this.breed = cat.breed;
    this.fluffiness = cat.fluffiness;
  }

  deleteCat(cat: Cat): void {
    this.catService.deleteCat(cat.id).subscribe({
      next: () => {
        this.successMessage = 'Кот удалён.';
        this.loadCats();
      },
      error: (error) => {
        this.errorMessage = 'Не удалось удалить кота.';
        console.error(error);
      },
    });
  }

  cancelEdit(): void {
    this.resetForm();
  }

  logout(): void {
    this.authService.logout();
    window.location.href = '/login';
  }

  private resetForm(): void {
    this.editingCatId = null;
    this.name = '';
    this.age = 1;
    this.breed = '';
    this.fluffiness = 1;
  }
}
