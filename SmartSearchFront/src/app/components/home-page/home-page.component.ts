import { Component, inject } from '@angular/core';
import { SearchLineComponent } from "../search-line/search-line.component";
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http'; // ← Добавьте эту строку
import { SearchServiceService } from '../../services/search-service/search-service.service';
import { PageInfo } from '../../interfaces/pageInfo';
import { Router } from '@angular/router';
import { InfoPageComponent } from "../info-page/info-page.component";
import { QueryResponseWithId } from '../../models/query-response';
import { RatingButtonComponent } from '../rating-button.component';
import { QueryResponseTableComponent } from '../query-response-table';

@Component({
  selector: 'app-home-page',
  imports: [SearchLineComponent, FormsModule, CommonModule, HttpClientModule, InfoPageComponent, RatingButtonComponent,
    QueryResponseTableComponent],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css',
  providers: [
    SearchServiceService // ← Добавьте сервис в providers
  ]
})
export class HomePageComponent {


onArticleClick(pageId: number) {
this.pageIsChosen = true;
    this.selectedPageId = pageId;
    console.log('Выбрана статья с ID:', pageId);
}

 selectedPageId: number | null = null; 

pageIsChosen: boolean = false;
searchResults: any ;
  isSearching: boolean = false;
  searchError: string = '';
 router = inject(Router);

  showRatingTable = false;
  queryResponses: QueryResponseWithId[] = [
    { id: 1, query: 'как дела', response: 'нормально', rating: 0 },
    { id: 2, query: 'сколько времени', response: '15:30', rating: 4 },
    { id: 3, query: 'какая погода', response: 'солнечно', rating: 0 },
    { id: 4, query: 'где находится', response: 'в офисе', rating: 2 }
  ];


 onSearchResults(results: PageInfo): void {
    this.searchResults = results;
     this.searchResults = [{
    id:1,
    largeName: "1211",
    previewText: "fff"

  }]
   this.pageIsChosen = false; 
  console.log(this.searchResults)
    this.isSearching = false;
    this.searchError = '';
    console.log('Результаты поиска:',  this.searchResults);

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
      
      // Здесь можно отправить данные на сервер
      // this.yourService.updateRating(updatedItem).subscribe();
    }
  }
}
