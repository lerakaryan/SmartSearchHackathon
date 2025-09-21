import { Injectable } from '@angular/core';
import { QueryResponseWithId } from '../../models/query-response';

@Injectable({
  providedIn: 'root'
})
export class HistoryService {
  private readonly STORAGE_KEY = 'search_history';

  constructor() {}

  // Сохранить новый запрос и ответ
  saveSearchHistory(query: string, response: any, selectedItem?: any): void {
    const history = this.getHistory();
    
    const newEntry: QueryResponseWithId = {
      id: Date.now(),
      query: query,
      response: this.formatResponse(response, selectedItem),
      rating: 0
    };

    history.unshift(newEntry);
    const limitedHistory = history.slice(0, 50);
    
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(limitedHistory));
  }

  // Получить всю историю
  getHistory(): QueryResponseWithId[] {
    const historyJson = localStorage.getItem(this.STORAGE_KEY);
    return historyJson ? JSON.parse(historyJson) : [];
  }

  // Обновить оценку
  updateRating(itemId: number, rating: number): void {
    const history = this.getHistory();
    const itemIndex = history.findIndex(item => item.id === itemId);
    
    if (itemIndex !== -1) {
      history[itemIndex].rating = rating;
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(history));
    }
  }

  // Форматирование ответа
  private formatResponse(response: any, selectedItem?: any): string {
    if (selectedItem) {
      return this.formatSelectedItem(selectedItem);
    }
    
    let result = '';
    
    if (response?.registry_records?.length > 0) {
      result += `Найдено контрактов/КС: ${response.registry_records.length}\n`;
    }
    
    if (response?.knowledge_base_articles?.length > 0) {
      result += `Найдено статей: ${response.knowledge_base_articles.length}\n`;
    }
    
    if (response?.intents) {
      result += `Предложено действие: ${response.intents.name}\n`;
    }
    
    return result || 'Ничего не найдено';
  }

  // Форматирование выбранного элемента
  private formatSelectedItem(item: any): string {
    if (item.type === 'registry') {
      if (item.hintType === 1) {
        return `Контракт: ${item.data.contractName} (${item.data.contractId})`;
      } else {
        return `КС: ${item.data.ksName} (${item.data.ksId})`;
      }
    } else if (item.type === 'knowledge_base') {
      return `Статья: ${item.text}`;
    } else if (item.name) {
      return `Действие: ${item.name}`;
    }
    
    return 'Выбранный элемент';
  }

  // Очистить историю
  clearHistory(): void {
    localStorage.removeItem(this.STORAGE_KEY);
  }
}