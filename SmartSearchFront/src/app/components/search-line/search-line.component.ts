import { CommonModule } from '@angular/common';
import { Component, Output, EventEmitter, inject, ViewChild, ElementRef, OnInit, AfterViewInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { SearchServiceService } from '../../services/search-service/search-service.service';
import { RawData } from '../../interfaces/rawData';
import { debounceTime, distinctUntilChanged, fromEvent, map, filter, switchMap, tap, catchError, of } from 'rxjs';
import { SearchResponse, RegistryHint, KnowledgeBaseHint, ActionHintIntents, RegistryHintType2, RegistryHintType1 } from '../../interfaces/hint';

@Component({
  selector: 'app-search-line',
  imports: [CommonModule, FormsModule],
  templateUrl: './search-line.component.html',
  styleUrl: './search-line.component.css'
})
export class SearchLineComponent implements AfterViewInit {
  searchTerm: string = '';
  isLoading: boolean = false;
  rawData: RawData = { text: '' };
  showSuggestions: boolean = false;
  
  suggestions: SearchResponse = {
    registry_records: [],
    knowledge_base_articles: [],
    intents: null
  };
  
  @Output() searchResults = new EventEmitter<SearchResponse>();
  @Output() searchStarted = new EventEmitter<void>();
  @Output() searchError = new EventEmitter<string>();
  @Output() suggestionSelected = new EventEmitter<any>();

   @Output() jsonGenerated = new EventEmitter<any>();
  lastGenerated: any = null;


  
  private emitJson(json: any) {
    this.lastGenerated = json;
    this.jsonGenerated.emit(json);
  }
  
  @ViewChild('searchInput') searchInput!: ElementRef;
  
  searchService = inject(SearchServiceService);
  selectedSuggestionIndex: number = -1;
  private lastQuery: string = '';

  ngAfterViewInit() {
    this.setupSearchInputListeners();
  }

  private setupSearchInputListeners() {
    // Проверяем, что searchInput инициализирован
    if (!this.searchInput?.nativeElement) {
      console.error('Search input element not found');
      return;
    }

    // Автопоиск при вводе с debounce
    fromEvent(this.searchInput.nativeElement, 'input')
      .pipe(
        map((event: any) => event.target.value.trim()),
        filter(query => query.length > 2),
        debounceTime(300),
        distinctUntilChanged(),
        tap(query => {
          this.lastQuery = query;
          this.isLoading = true;
          this.showSuggestions = true;
        }),
        switchMap(query => 
          this.searchService.sendData({ text: query }).pipe(
            catchError(error => {
              this.isLoading = false;
              this.searchError.emit('Ошибка загрузки подсказок');
              console.error('Suggestions error:', error);
              return of({
                registry_records: [],
                knowledge_base_articles: [],
                intents: null
              } as SearchResponse);
            })
          )
        )
      )
      .subscribe((response: SearchResponse) => {
        this.isLoading = false;
        this.suggestions = response;
        this.showSuggestions = this.hasSuggestions();
      });

    // Навигация по подсказкам клавишами
    fromEvent(this.searchInput.nativeElement, 'keydown')
      .subscribe((event: any) => {
        if (!this.showSuggestions) return;

        const totalSuggestions = this.getTotalSuggestionsCount();

        switch (event.key) {
          case 'ArrowDown':
            event.preventDefault();
            this.selectedSuggestionIndex = 
              this.selectedSuggestionIndex < totalSuggestions - 1 
                ? this.selectedSuggestionIndex + 1 
                : 0;
            break;
          case 'ArrowUp':
            event.preventDefault();
            this.selectedSuggestionIndex = 
              this.selectedSuggestionIndex > 0 
                ? this.selectedSuggestionIndex - 1 
                : totalSuggestions - 1;
            break;
          case 'Enter':
            if (this.selectedSuggestionIndex >= 0) {
              event.preventDefault();
              this.selectSuggestionByIndex(this.selectedSuggestionIndex);
            }
            break;
          case 'Escape':
            this.hideSuggestions();
            break;
        }
      });

    // Скрываем подсказки при клике вне области
    fromEvent(document, 'click')
      .subscribe((event: any) => {
        if (this.searchInput.nativeElement && !this.searchInput.nativeElement.contains(event.target)) {
          this.hideSuggestions();
        }
      });
  }

  // Сделал публичным для использования в шаблоне
  hasSuggestions(): boolean {
    return this.suggestions.registry_records.length > 0 ||
           this.suggestions.knowledge_base_articles.length > 0 ||
           (this.suggestions.intents !== null && this.suggestions.intents.name !== '');
  }

  // Сделал публичным для использования в шаблоне
  getTotalSuggestionsCount(): number {
    return this.suggestions.registry_records.length +
           this.suggestions.knowledge_base_articles.length +
           (this.suggestions.intents !== null ? 1 : 0);
  }

  // Получение подсказки по индексу с учетом всех типов
  private getSuggestionByIndex(index: number): any {
    const registryCount = this.suggestions.registry_records.length;
    const knowledgeCount = this.suggestions.knowledge_base_articles.length;

    if (index < registryCount) {
      return this.suggestions.registry_records[index];
    } else if (index < registryCount + knowledgeCount) {
      return this.suggestions.knowledge_base_articles[index - registryCount];
    } else if (this.suggestions.intents !== null) {
      return this.suggestions.intents;
    }
    return null;
  }

  // Генерация текста для отображения подсказки
  getSuggestionText(suggestion: any): string {
    if (this.isRegistryHint(suggestion)) {
      const data = suggestion.data;
      if (suggestion.hintType === 1) {
        return `Контракт: ${(data as any).contractName} (${(data as any).contractId})`;
      } else {
        return `КС: ${(data as any).ksName} (${(data as any).ksId})`;
      }
    } else if (this.isKnowledgeBaseHint(suggestion)) {
      return `База знаний: ${suggestion.text}`;
    } else if (this.isIntent(suggestion)) {
      return `Действие: ${suggestion.name}`;
    }
    return '';
  }

  // Вспомогательные методы проверки типов
  private isRegistryHint(item: any): item is RegistryHint {
    return item && item.type === 'registry';
  }

  private isKnowledgeBaseHint(item: any): item is KnowledgeBaseHint {
    return item && item.type === 'knowledge_base';
  }

  private isIntent(item: any): item is ActionHintIntents {
    return item && item.name !== undefined;
  }

  selectSuggestionByIndex(index: number) {
    const suggestion = this.getSuggestionByIndex(index);
    if (suggestion) {
      this.selectSuggestion(suggestion);
    }
  }

  selectSuggestion(suggestion: any) {
    this.suggestionSelected.emit(suggestion);
   
  
    if (suggestion.type === 'registry') {
      if (suggestion.hintType === 1) {
        const data = suggestion.data as RegistryHintType1['data'];
        this.searchTerm = data.contractName;
      } else {
        const data = suggestion.data as RegistryHintType2['data'];
        this.searchTerm = data.ksName;
      }
    } else if (suggestion.type === 'knowledge_base') {
      this.searchTerm = suggestion.text;
    } else if (suggestion.name) {
      this.searchTerm = suggestion.name;
    }
     this.emitJson(suggestion);
    this.hideSuggestions();
  }

  onSearch(): void {
    if (!this.searchTerm.trim()) return;

    this.isLoading = true;
    this.searchStarted.emit();
    this.hideSuggestions();

    this.rawData.text = this.searchTerm;
    this.searchService.sendData(this.rawData)
      .subscribe({
        next: (response: SearchResponse) => {
          this.isLoading = false;
          this.searchResults.emit(response);
        },
        error: (error) => {
          this.isLoading = false;
          this.searchError.emit('Ошибка при поиске');
          console.error('Search error:', error);
        }
      });
  }

  clearSearch(): void {
    this.searchTerm = '';
    this.rawData.text = '';
    this.searchResults.emit({
      registry_records: [],
      knowledge_base_articles: [],
      intents: null
    });
    this.hideSuggestions();
  }

  hideSuggestions() {
    this.showSuggestions = false;
    this.selectedSuggestionIndex = -1;
  }

  // Для отладки
  get debugInfo() {
    return {
      registry: this.suggestions.registry_records.length,
      knowledge: this.suggestions.knowledge_base_articles.length,
      intents: this.suggestions.intents !== null ? 1 : 0
    };
  }
}