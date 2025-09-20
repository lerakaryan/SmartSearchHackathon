import { CommonModule } from '@angular/common';
import { Component, Output, EventEmitter, inject, ViewChild, ElementRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { SearchServiceService } from '../../services/search-service/search-service.service';
import { RawData } from '../../interfaces/rawData';
import { debounceTime, distinctUntilChanged, fromEvent, map } from 'rxjs';
import { BaseHint, SearchResponse } from '../../interfaces/hint';

@Component({
  selector: 'app-search-line',
  imports: [CommonModule, FormsModule],
  templateUrl: './search-line.component.html',
  styleUrl: './search-line.component.css'
})
export class SearchLineComponent {
  searchTerm: string = '';
  isLoading: boolean = false;
rawData: RawData = { text: '' };
 showSuggestions: boolean = false;
  suggestions!: SearchResponse; 
  @Output() searchResults = new EventEmitter<any>();
  @Output() searchStarted = new EventEmitter<void>();
  @Output() searchError = new EventEmitter<string>();
@ViewChild('searchInput') searchInput!: ElementRef;
  searchService = inject(SearchServiceService);
 @Output() suggestionSelected = new EventEmitter<any>(); // Событие выбора подсказки
  selectedSuggestionIndex: number = -1;

  ngAfterViewInit() {
    // Автопоиск при вводе
    fromEvent(this.searchInput.nativeElement, 'input')
      .pipe(
        map((event: any) => event.target.value),
        debounceTime(200), // Уменьшил задержку для более быстрого отклика
        distinctUntilChanged()
      )
      .subscribe((value: string) => {
        if (value.trim().length > 0) {
          this.showSuggestionsForQuery(value);
        } else {
          this.hideSuggestions();
        }
      });

    // Навигация по подсказкам
    // fromEvent(this.searchInput.nativeElement, 'keydown')
    //   .subscribe((event: any) => {
    // //    if (this.showSuggestions && this.suggestions.length > 0) {
    //       switch (event.key) {
    //         case 'ArrowDown':
    //           event.preventDefault();
    //           this.selectNextSuggestion();
    //           break;
    //         case 'ArrowUp':
    //           event.preventDefault();
    //           this.selectPreviousSuggestion();
    //           break;
    //         case 'Enter':
    //           event.preventDefault();
    //           if (this.selectedSuggestionIndex >= 0) {
    //            // this.selectSuggestion(this.suggestions[this.selectedSuggestionIndex]);
    //           }
    //           break;
    //         case 'Escape':
    //           this.hideSuggestions();
    //           break;
    //       }
    //     }
    //  // }
    // );
  }


  
showSuggestionsForQuery(query: string) {
  this.onSearch();
  console.log(this.suggestions + "faadfaf");
 

  console.log('Найдены подсказки:', this.suggestions);
 // this.showSuggestions = this.suggestions.length > 0;
  this.selectedSuggestionIndex = -1;
}
  
 selectSuggestion(suggestion: any) {
    this.suggestionSelected.emit(suggestion); // Отправляем выбранную подсказку
    this.searchTerm= suggestion.largeName; // Заполняем поле выбранной подсказкой
    this.hideSuggestions();
  }

  // selectNextSuggestion() {
  //   if (this.selectedSuggestionIndex < this.suggestions.length - 1) {
  //     this.selectedSuggestionIndex++;
  //   } else {
  //     this.selectedSuggestionIndex = 0;
  //   }
  // }

  // selectPreviousSuggestion() {
  //   if (this.selectedSuggestionIndex > 0) {
  //     this.selectedSuggestionIndex--;
  //   } else {
  //     this.selectedSuggestionIndex = this.suggestions.length - 1;
  //   }
  // }

  hideSuggestions() {
    this.showSuggestions = false;
    this.selectedSuggestionIndex = -1;
  }

   onSearch(): void {
    if (!this.searchTerm.trim()) return;

    this.isLoading = true;
    this.searchStarted.emit();

    this.rawData.text = this.searchTerm;
    this.searchService.sendData(this.rawData) 
      .subscribe({
        next: (response: SearchResponse) => {
          console.log(response + " response");
          this.isLoading = false;
          this.searchResults.emit(response);
          this.suggestions = response;
          
          // Теперь это будет работать
          console.log(this.suggestions.registry_records, "registry records");
          
          if (this.suggestions.registry_records.length > 0) {
            console.log(this.suggestions.registry_records[0], "first registry record");
          }
          
          console.log(this.suggestions.knowledge_base_articles, "knowledge base articles");
          console.log(this.suggestions.intents, "intents");
        },
        error: (error) => {
          this.isLoading = false;
          this.searchError.emit('Ошибка при поиске');
          console.error('Search error:', error);
        }
      });
  }

  searchOne(){
    
  }

  onKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      this.searchOne();
    }
    else
      {
           this.onSearch();
      }
  }

   clearSearch(): void {
    this.searchTerm = '';
    this.rawData.text = ''; // очищаем и rawData
    this.searchResults.emit(null);
  }

    // private getSearchResults(query: string): any[] {
    // // Замените на реальный API вызов
    // const mockData = [
    //   { id: 1, largeName: "Angular разработка", previewText: "Руководство по Angular разработке" },
    //   { id: 2, largeName: "React vs Angular", previewText: "Сравнение фреймворков 2024" },
    //   { id: 3, largeName: "JavaScript основы", previewText: "Основы JavaScript для начинающих" },
    //   { id: 4, largeName: "TypeScript преимущества", previewText: "Почему выбирают TypeScript" },
    //   { id: 5, largeName: "Веб разработка 2024", previewText: "Новые тренды веб разработки" }
    // ];

  //  return mockData.filter(item => 
  //     item.largeName.toLowerCase().includes(query.toLowerCase()) ||
  //     item.previewText.toLowerCase().includes(query.toLowerCase())
  //   );
  // }

}
