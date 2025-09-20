import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { RawData } from '../../interfaces/rawData';


@Injectable({
  providedIn: 'root'
})
export class SearchServiceService {
private apiUrl = environment.apiUrl +'/pages';
http = inject(HttpClient);
  constructor() { }

  sendData(rawData: RawData) 
  {
    console.log(rawData);
    return this.http.post(this.apiUrl, rawData); //тут ответ список статей
  }

  getPageById(id: number)
{
return this.http.get(this.apiUrl+'/'+id);
}

}
