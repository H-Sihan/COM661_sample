import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ItemService } from '../../services/item.service';

@Component({
  selector: 'app-item-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './item-list.component.html',
  styleUrls: ['./item-list.component.css'],
})
export class ItemListComponent implements OnInit {
  items: any[] = [];

  constructor(private itemService: ItemService) {}

  ngOnInit(): void {
    this.fetchItems();
  }

  fetchItems() {
    this.itemService.getItems().subscribe(
      (data) => {
        this.items = data;
      },
      (error) => {
        console.error('Error fetching items:', error);
        alert('Failed to fetch items. Please try again later.');
      }
    );
  }

  deleteItem(id: string) {
    if (confirm('Are you sure you want to delete this item?')) {
      this.itemService.deleteItem(id).subscribe(
        () => {
          alert('Item deleted successfully!');
          this.fetchItems();
        },
        (error) => {
          console.error('Error deleting item:', error);
          alert('Failed to delete item. Please try again later.');
        }
      );
    }
  }
}
