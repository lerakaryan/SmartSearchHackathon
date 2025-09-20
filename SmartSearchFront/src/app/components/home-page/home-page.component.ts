import { Component } from '@angular/core';
import { SearchLineComponent } from "../search-line/search-line.component";
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http'; // ← Добавьте эту строку
import { SearchServiceService } from '../../services/search-service/search-service.service';

@Component({
  selector: 'app-home-page',
  imports: [SearchLineComponent, FormsModule, CommonModule,HttpClientModule],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css',
  providers: [
    SearchServiceService // ← Добавьте сервис в providers
  ]
})
export class HomePageComponent {
searchResults: any = null;
  isSearching: boolean = false;
  searchError: string = '';


 onSearchResults(results: any): void {
    this.searchResults = results;
    this.isSearching = false;
    this.searchError = '';
    console.log('Результаты поиска:', results);

  }

    // Обработчик начала поиска
  onSearchStarted(): void {
    this.isSearching = true;
    this.searchError = '';
    this.searchResults = null;
  }

  // Обработчик ошибок поиска
  onSearchError(error: string): void {
    this.searchError = error;
    this.isSearching = false;
  }
}
