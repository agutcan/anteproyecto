import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  base = '/api/';

  constructor(private http: HttpClient) {}

  private headers(){
    const token = localStorage.getItem('access_token');
    const h: any = { 'Content-Type': 'application/json' };
    if(token) { h['Authorization'] = `Bearer ${token}` }
    return new HttpHeaders(h);
  }

  get(path: string): Observable<any>{
    return this.http.get(this.base + path, { headers: this.headers() });
  }

  post(path: string, body: any){
    return this.http.post(this.base + path, body, { headers: this.headers() });
  }
}
