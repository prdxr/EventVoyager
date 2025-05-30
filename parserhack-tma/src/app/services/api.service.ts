import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {map, Observable} from 'rxjs';

declare var endpoint: string;
declare var token: string;

export interface IEventTag {
  tag_code: number;
  description: string;
}

export interface IEventType {
  type_code: number;
  description: string;
}

export interface IApiRow {
  id: number;
  tags: IEventTag[];
  type_of_event: IEventType;
  title: string;
  description: string;
  addresses: string;
  start_date: string;
  registration_deadline: string;
  end_date: string;
  url: string;
  is_free: boolean;
}

export type TApiData = IApiRow[];

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  public apiEndpoint = endpoint || '';
  public authToken: string = token || '';
  public isLoading = false;

  constructor(
    private http: HttpClient
  ) {
  }

  // public initialize(): any {
  //   const authEndpoint = this.apiEndpoint + '/auth/token/login/';
  //   alert(authEndpoint);
  //   const result = this.http.post(authEndpoint,
  //     {
  //       "username": "root",
  //       "password": "root"
  //     }
  //   );
  //   result.subscribe(data => { console.log(data); });
  //   return result;
  // }

  public getData(): Observable<TApiData> {
    const action = this.apiEndpoint + '/hackaton/';
    this.isLoading = true;
    const result = this.http.get<any[]>(action);
    result.subscribe(() => this.isLoading = false);
    return result;
  }
}
