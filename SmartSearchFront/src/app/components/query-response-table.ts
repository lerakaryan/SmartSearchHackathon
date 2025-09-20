import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export interface QueryResponseWithId {
  id: number;
  query: string;
  response: string;
  rating: number;
}

@Component({
  selector: 'app-query-response-table',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="table-container">
      <table class="query-response-table">
        <thead>
          <tr>
            <th>Запрос</th>
            <th>Ответ</th>
            <th>Оценка</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let item of data; trackBy: trackByFn" class="table-row">
            <td class="query-cell">{{ item.query }}</td>
            <td class="response-cell">{{ item.response }}</td>
            <td class="rating-cell">
              <span *ngIf="item.rating > 0" class="rating-display">
                {{ item.rating }}
              </span>
              <span *ngIf="item.rating === 0" class="no-rating">
                Нет оценки
              </span>
            </td>
            <td class="actions-cell">
              <div *ngIf="item.rating === 0; else ratedTemplate">
                <select 
                  #ratingSelect
                  (change)="onRatingChange(item, ratingSelect.value)"
                  class="rating-select"
                >
                  <option value="">Выберите оценку</option>
                  <option *ngFor="let rating of ratings" [value]="rating">
                    {{ rating }}
                  </option>
                </select>
              </div>
              <ng-template #ratedTemplate>
                <span class="rated-text">Оценено</span>
              </ng-template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  `,
  styles: [`
    .table-container {
      width: 100%;
      overflow-x: auto;
    }

    .query-response-table {
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0;
      font-family: Arial, sans-serif;
    }

    .query-response-table th {
      background-color: #f5f5f5;
      padding: 12px;
      text-align: left;
      font-weight: bold;
      border-bottom: 2px solid #ddd;
    }

    .query-response-table td {
      padding: 12px;
      border-bottom: 1px solid #eee;
    }

    .table-row:hover {
      background-color: #f9f9f9;
    }

    .query-cell {
      min-width: 200px;
      max-width: 300px;
      word-wrap: break-word;
    }

    .response-cell {
      min-width: 300px;
      max-width: 500px;
      word-wrap: break-word;
    }

    .rating-cell {
      width: 100px;
      text-align: center;
    }

    .rating-display {
      font-weight: bold;
      color: #007bff;
    }

    .no-rating {
      color: #6c757d;
      font-style: italic;
    }

    .actions-cell {
      width: 150px;
    }

    .rating-select {
      padding: 6px 12px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 14px;
    }

    .rated-text {
      color: #28a745;
      font-weight: bold;
    }
  `]
})
export class QueryResponseTableComponent {
  @Input() data: QueryResponseWithId[] = [];
  @Output() ratingChange = new EventEmitter<QueryResponseWithId>();

  ratings = [1, 2, 3, 4, 5];

  onRatingChange(item: QueryResponseWithId, newRating: string): void {
    const ratingNumber = parseInt(newRating, 10);
    if (!isNaN(ratingNumber)) {
      const updatedItem = { ...item, rating: ratingNumber };
      this.ratingChange.emit(updatedItem);
    }
  }

  trackByFn(index: number, item: QueryResponseWithId): number {
    return item.id;
  }
}