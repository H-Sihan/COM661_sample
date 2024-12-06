import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ItemService } from '../../services/item.service';

@Component({
  selector: 'app-item-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './item-form.component.html',
  styleUrls: ['./item-form.component.css'],
})
export class ItemFormComponent implements OnInit {
  item: any = { name: '', quantity: 0, value: 0 };
  isUpdate = false;

  constructor(
    private itemService: ItemService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isUpdate = true;
      this.fetchItem(id);
    }
  }

  fetchItem(id: string) {
    this.itemService.getItems().subscribe(
      (data) => {
        const foundItem = data.find((item: any) => item._id === id);
        if (foundItem) {
          this.item = foundItem;
        } else {
          alert('Item not found');
          this.router.navigate(['/']);
        }
      },
      (error) => {
        console.error('Error fetching item:', error);
      }
    );
  }

  saveItem() {
    if (!this.item.name || this.item.quantity <= 0 || this.item.value <= 0) {
      alert('Please fill all fields correctly!');
      return;
    }
  
    const payload = {
      name: this.item.name,
      quantity: this.item.quantity,
      value: this.item.value,
    };
  
    if (this.isUpdate) {
      console.log('Updating item with payload:', payload);
      this.itemService.updateItem(this.item._id, payload).subscribe(
        (response) => {
          console.log('Update successful:', response);
          alert('Item updated successfully!');
          this.router.navigate(['/']);
        },
        (error) => {
          console.error('Error updating item:', error);
          alert('Failed to update item. Check the console for more details.');
        }
      );
    } else {
      console.log('Adding new item with payload:', payload);
      this.itemService.addItem(payload).subscribe(
        (response) => {
          console.log('Item added successfully:', response);
          alert('Item added successfully!');
          this.router.navigate(['/']);
        },
        (error) => {
          console.error('Error adding item:', error);
        }
      );
    }
  }  
}