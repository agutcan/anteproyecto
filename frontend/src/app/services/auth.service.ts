import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class AuthService {
  constructor(private http: HttpClient) {}

  login(username: string, password: string){
    return this.http.post('/api/token/', { username, password }).pipe(
      tap((res: any) => {
        if(res.access){
          localStorage.setItem('access_token', res.access);
        }
        if(res.refresh){
          localStorage.setItem('refresh_token', res.refresh);
        }
      })
    )
  }

  logout(){
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
}
