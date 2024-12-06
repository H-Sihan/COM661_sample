import { Routes } from '@angular/router';
import { ItemListComponent } from './components/item-list/item-list.component';
import { ItemFormComponent } from './components/item-form/item-form.component';

export const routes: Routes = [
  { path: '', component: ItemListComponent }, // Default route
  { path: 'add-item', component: ItemFormComponent }, // Add item route
  { path: 'update-item/:id', component: ItemFormComponent }, // Update item route
];
