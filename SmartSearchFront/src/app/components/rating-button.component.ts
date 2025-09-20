import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-rating-button',
  template: `
    <div class="rating-button-container">
      <button 
        class="rating-toggle-button"
        (click)="toggleTable()"
        [class.active]="isOpen"
      >
        {{ isOpen ? '✕' : '⭐' }} Оценить ответы
      </button>
    </div>
  `,
  styles: [`
    .rating-button-container {
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 1000;
    }

    .rating-toggle-button {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 25px;
      padding: 12px 24px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .rating-toggle-button:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }

    .rating-toggle-button.active {
      background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    }
  `]
})
export class RatingButtonComponent {
  @Output() buttonClick = new EventEmitter<void>();
  isOpen = false;

  toggleTable(): void {
    this.isOpen = !this.isOpen;
    this.buttonClick.emit();
  }
}