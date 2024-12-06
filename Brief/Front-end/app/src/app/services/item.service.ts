import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ItemService {
  private apiUrl: string;

  constructor(
    private http: HttpClient,
    @Inject('BASE_API_URL') private baseApiUrl: string
  ) {
    this.apiUrl = `${this.baseApiUrl}/items`; // Define the base API endpoint
  }

  // Fetch all items
  getItems(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  // Add a new item
  addItem(item: any): Observable<any> {
    return this.http.post(this.apiUrl, item);
  }

  // Update an item by ID
  updateItem(id: string, item: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, item);
  }

  // Delete an item by ID
  deleteItem(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
