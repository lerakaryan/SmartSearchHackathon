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
pageData!: PageInfo ;
  loading: boolean = false;
  error: string | null = null;
  
 constructor(
    private route: ActivatedRoute,
    private searchService: SearchServiceService
  ) {}

   ngOnInit(): void {
   }

  
}
