import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { RawData } from '../../interfaces/rawData';
import { PageInfo } from '../../interfaces/pageInfo';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class SearchServiceService {
private apiUrl = environment.apiUrl +'/pages';
http = inject(HttpClient);
  constructor() { }

  sendData(rawData: RawData): Observable<PageInfo[]>
  {
    console.log(rawData);
    return this.http.post<PageInfo[]>(this.apiUrl, rawData); //тут ответ список статей
  }

  getPageById(id: number): Observable<PageInfo>
{
return this.http.get<PageInfo>(this.apiUrl+'/'+id);
}

}
