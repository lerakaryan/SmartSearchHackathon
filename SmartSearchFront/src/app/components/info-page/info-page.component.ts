import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { PageInfo } from '../../interfaces/pageInfo';
import { ActivatedRoute } from '@angular/router';

import { catchError, of } from 'rxjs';
import { SearchServiceService } from '../../services/search-service/search-service.service';

@Component({
  selector: 'app-info-page',
  imports: [FormsModule, CommonModule],
  templateUrl: './info-page.component.html',
  styleUrl: './info-page.component.css'
})
export class InfoPageComponent {
pageData: PageInfo | null = null;
  loading: boolean = false;
  error: string | null = null;
  
 constructor(
    private route: ActivatedRoute,
    private searchService: SearchServiceService;
  ) {}

   ngOnInit(): void {
    this.loadPageData();
  }

   loadPageData(): void {
    this.loading = true;
    this.error = null;

    this.route.params.subscribe(params => {
      const pageId = params['id'];
      
      if (pageId) {
        this.pageDataService.getPageById(+pageId)
          .pipe(
            catchError(error => {
              this.loading = false;
              this.error = 'Ошибка загрузки страницы';
              console.error('Error loading page:', error);
              return of(null);
            })
          )
          .subscribe((response: PageInfo | null) => {
            this.loading = false;
            
            if (response && response.items && response.items.length > 0) {
              this.pageData = response.items[0];
            } else {
              this.error = 'Страница не найдена';
            }
          });
      } else {
        this.loading = false;
        this.error = 'ID страницы не указан';
      }
    });
  }
}
