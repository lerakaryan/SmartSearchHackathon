import { Component, EventEmitter, Input, Output } from '@angular/core';
import {  QueryResponse, QueryResponseWithId } from '../../models/query-response';

@Component({
  selector: 'app-list-history',
  imports: [],
  templateUrl: './list-history.component.html',
  styleUrl: './list-history.component.css'
})
export class ListHistoryComponent {
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
