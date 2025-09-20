import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { RawData } from '../../interfaces/rawData';

import { Observable } from 'rxjs';
import { Hint } from '../../interfaces/hint';


@Injectable({
  providedIn: 'root'
})
export class SearchServiceService {
private apiUrl = environment.apiUrl +'/predict';
http = inject(HttpClient);
  constructor() { }

  sendData(rawData: RawData): Observable<Hint[]>
  {
    console.log(rawData);
    return this.http.post<Hint[]>(this.apiUrl, rawData); //тут ответ список статей
  }

  getPageById(id: number): Observable<Hint>
{
return this.http.get<Hint>(this.apiUrl+'/'+id);
}

}
