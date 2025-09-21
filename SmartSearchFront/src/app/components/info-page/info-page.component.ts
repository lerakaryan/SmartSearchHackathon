import { CommonModule } from '@angular/common';
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
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
  
@Input() jsonData: any = null;
  receivedTime: Date | null = null;
isKs: boolean = false;
ifKnowledge: boolean = false;
isAction: boolean = false;
isSupport: boolean = false;



  ngOnChanges(changes: SimpleChanges) {
    if (changes['jsonData'] && changes['jsonData'].currentValue) {
      this.receivedTime = new Date();
    }
  }

  getDataType(): string {
    if (!this.jsonData) return 'Нет данных';
    return Array.isArray(this.jsonData) ? 'Массив' : 'Объект';
  }

 constructor(
    private route: ActivatedRoute,
   
  ) {}

   ngOnInit(): void {
   console.log(this.jsonData, "ffff");
   }

   loadPageData(): void {
  
    // this.route.params.subscribe(params => {
    //   const pageId = params['id'];
      
    //   // if (pageId) {
    //   //   this.pageDataService.getPageById(+pageId)
    //   //     .pipe(
    //   //       catchError(error => {
    //   //         this.loading = false;
    //   //         this.error = 'Ошибка загрузки страницы';
    //   //         console.error('Error loading page:', error);
    //   //         return of(null);
    //   //       })
    //   //     )
    //       // .subscribe((response: PageInfo | null) => {
    //       //   this.loading = false;
            
    //       //   if (response && response.items && response.items.length > 0) {
    //       //     this.pageData = response.items[0];
    //       //   } else {
    //       //     this.error = 'Страница не найдена';
    //       //   }
    //       // });
    //   } else {
    //     this.loading = false;
    //     this.error = 'ID страницы не указан';
    //   }
    // });
  }
}
