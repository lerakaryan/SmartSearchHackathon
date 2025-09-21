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
isKnowledge: boolean = false;
isAction: boolean = false;
isSupport: boolean = false;



  ngOnChanges(changes: SimpleChanges) {
    if (changes['jsonData'] && changes['jsonData'].currentValue) {
      this.receivedTime = new Date();
    }
  }

  getType(): string {
    if (!this.jsonData) return 'Нет данных';

    this.isKs = false;
    this.isKnowledge = false;
    this.isAction = false;
    this.isSupport = false;
    if(Array.isArray(this.jsonData))
      {
        this.isKnowledge = true;
      }
      else 
      {
        if (this.jsonData.type !=null)
          {
             this.isKs = true;
          }
          else
            {
              if(this.jsonData.name == "unknown")
                {
                  this.isSupport = true;
                }
                else{
              this.isAction = true;
                }
            }
      }
   
      console.log(this.isAction, this.isKnowledge, this.isKs, this.isSupport)
      return "";
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
