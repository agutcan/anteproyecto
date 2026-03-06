import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-game-list',
  templateUrl: './game-list.component.html',
  styleUrls: ['./game-list.component.scss']
})
export class GameListComponent implements OnInit {
  games: any[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit(){
    this.api.get('games/').subscribe({
      next: (res:any) => { this.games = res; this.loading = false },
      error: () => { this.loading = false }
    })
  }
}
