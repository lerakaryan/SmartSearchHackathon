import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PageDataService {

private apiUrl = environment.apiUrl +'/pages/';

getPageById(id: number)
{
return this.http.get(this.apiUrl+id);
}



  constructor(private http: HttpClient) { }
}
