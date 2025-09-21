import { Component, inject } from '@angular/core';
import { SearchLineComponent } from "../search-line/search-line.component";
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http'; // ← Добавьте эту строку
import { SearchServiceService } from '../../services/search-service/search-service.service';

import { Router } from '@angular/router';
import { QueryResponseWithId } from '../../models/query-response';
import { RatingButtonComponent } from '../rating-button.component';
import { QueryResponseTableComponent } from '../query-response-table';
import { RegistryHint, SearchResponse } from '../../interfaces/hint';
import { InfoPageComponent } from "../info-page/info-page.component";


@Component({
  selector: 'app-home-page',
  imports: [SearchLineComponent, FormsModule, CommonModule, HttpClientModule, RatingButtonComponent,
    QueryResponseTableComponent, InfoPageComponent],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css',
  providers: [
    SearchServiceService // ← Добавьте сервис в providers
  ]
})
export class HomePageComponent {
  selectedPageId: number | null = null; 
  pageIsChosen: boolean = false;
  searchResponse: SearchResponse | null = null;
  isSearching: boolean = false;


  
  isSomethingChoosen: boolean = false;
  currentJson: any = null;

   onJsonGenerated(jsonData: any) {
    this.currentJson = jsonData;
    this.isSomethingChoosen= true;
  }


  searchError: string = '';
  router = inject(Router);

  showRatingTable = false;
  queryResponses: QueryResponseWithId[] = [
    { id: 1, query: 'как дела', response: 'нормально', rating: 0 },
    { id: 2, query: 'сколько времени', response: '15:30', rating: 4 },
    { id: 3, query: 'какая погода', response: 'солнечно', rating: 0 },
    { id: 4, query: 'где находится', response: 'в офисе', rating: 2 }
  ];

  // Обработчик результатов поиска
  onSearchResults(response: SearchResponse): void {
    this.searchResponse = response;
    this.pageIsChosen = false; 
    this.isSearching = false;
    this.searchError = '';
    console.log('Результаты поиска:', this.searchResponse);
  }

  // Обработчик выбора подсказки
  onSuggestionSelected(suggestion: any): void {
    this.pageIsChosen = true;
    if (suggestion.type === 'registry') {
      this.selectedPageId = suggestion.hintType === 1 
        ? parseInt(this.getContractId(suggestion)) 
        : parseInt(this.getKsId(suggestion));
    } else if (suggestion.type === 'knowledge_base') {
      this.selectedPageId = this.generateIdFromText(suggestion.text);
    } else if (suggestion.name) {
      this.selectedPageId = this.generateIdFromText(suggestion.name);
    }
    console.log('Выбрана подсказка:', suggestion);
  }

  // Обработчик клика по статье
  onArticleClick(pageId: number): void {
    this.pageIsChosen = true;
    this.selectedPageId = pageId;
    console.log('Выбрана статья с ID:', pageId);
  }

  // Обработчик начала поиска
  onSearchStarted(): void {
    this.isSearching = true;
    this.searchError = '';
    this.pageIsChosen = false; 
  }

  // Обработчик ошибок поиска
  onSearchError(error: string): void {
    this.pageIsChosen = false; 
    this.searchError = error;
    this.isSearching = false;
  }

  onRatingButtonClick(): void {
    this.showRatingTable = !this.showRatingTable;
  }

onRatingChange(updatedItem: QueryResponseWithId): void {
    const index = this.queryResponses.findIndex(item => item.id === updatedItem.id);
    if (index !== -1) {
      this.queryResponses[index] = updatedItem;
      console.log('Оценка обновлена:', updatedItem);
    }
  }

  // Новые методы для шаблона
  getRecordType(record: RegistryHint): string {
    return record.hintType === 1 ? 'Контракт' : 'КС';
  }

  getRecordId(record: RegistryHint): string {
    return record.hintType === 1 
      ? (record.data as any).contractId 
      : (record.data as any).ksId;
  }

  getContractId(record: any): string {
    return (record.data as any).contractId;
  }

  getKsId(record: any): string {
    return (record.data as any).ksId;
  }

  // Вспомогательный метод для генерации ID из текста
  private generateIdFromText(text: string): number {
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
      hash = ((hash << 5) - hash) + text.charCodeAt(i);
      hash = hash & hash;
    }
    return Math.abs(hash);
  }

  // Вспомогательный метод для отображения реестровых записей
  getRegistryPreview(record: RegistryHint): string {
    if (record.hintType === 1) {
      const data = record.data as any;
      return `Контракт: ${data.contractName} (${data.contractId})`;
    } else {
      const data = record.data as any;
      return `КС: ${data.ksName} (${data.ksId})`;
    }
  }

  // Метод для получения общего количества результатов
  getTotalResultsCount(): number {
    if (!this.searchResponse) return 0;
    
    return this.searchResponse.registry_records.length +
           this.searchResponse.knowledge_base_articles.length +
           (this.searchResponse.intents ? 1 : 0);
  }
}