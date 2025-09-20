import { Component, inject } from '@angular/core';
import { SearchLineComponent } from "../search-line/search-line.component";
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http'; // ← Добавьте эту строку
import { SearchServiceService } from '../../services/search-service/search-service.service';
import { PageInfo } from '../../interfaces/pageInfo';
import { Router } from '@angular/router';
import { InfoPageComponent } from "../info-page/info-page.component";

@Component({
  selector: 'app-home-page',
  imports: [SearchLineComponent, FormsModule, CommonModule, HttpClientModule, InfoPageComponent],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css',
  providers: [
    SearchServiceService // ← Добавьте сервис в providers
  ]
})
export class HomePageComponent {


 

  onSuggestionSelected(suggestion: any) {
    this.pageIsChosen = true;
    this.selectedPageId = suggestion.id;
    console.log('Выбрана статья:', suggestion);
  }
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


 
}
