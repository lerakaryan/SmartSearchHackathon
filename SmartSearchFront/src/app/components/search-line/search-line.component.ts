import { CommonModule } from '@angular/common';
import { Component, Output, EventEmitter, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { SearchServiceService } from '../../services/search-service/search-service.service';
import { RawData } from '../../interfaces/rawData';

@Component({
  selector: 'app-search-line',
  imports: [CommonModule, FormsModule],
  templateUrl: './search-line.component.html',
  styleUrl: './search-line.component.css'
})
export class SearchLineComponent {
  searchTerm: string = '';
  isLoading: boolean = false;
rawData: RawData = { data: '' };
  @Output() searchResults = new EventEmitter<any>();
  @Output() searchStarted = new EventEmitter<void>();
  @Output() searchError = new EventEmitter<string>();

  searchService = inject(SearchServiceService);

    onSearch(): void {
    if (!this.searchTerm.trim()) return;

    this.isLoading = true;
    this.searchStarted.emit(); // Уведомляем о начале поиска

    this.rawData.data = this.searchTerm;
    this.searchService.sendData(this.rawData) 
      .subscribe({
        next: (response) => {
          this.isLoading = false;
          this.searchResults.emit(response); // Отправляем результаты
        },
        error: (error) => {
          this.isLoading = false;
          this.searchError.emit('Ошибка при поиске');
        }
      });
  }

  onKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      this.onSearch();
    }
  }

   clearSearch(): void {
    this.searchTerm = '';
    this.rawData.data = ''; // очищаем и rawData
    this.searchResults.emit(null);
  }
}
