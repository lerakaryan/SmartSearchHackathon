import { Routes } from '@angular/router';
import { SearchLineComponent } from './components/search-line/search-line.component';
import { HomePageComponent } from './components/home-page/home-page.component';

export const routes: Routes = [

    {path: 'search', component: SearchLineComponent},
    {path: '', component: HomePageComponent}
];
