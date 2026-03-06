import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { GameListComponent } from './components/game-list/game-list.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'games', component: GameListComponent },
];
