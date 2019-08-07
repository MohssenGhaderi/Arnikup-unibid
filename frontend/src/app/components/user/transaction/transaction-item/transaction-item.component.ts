import { Component, OnInit, Input } from '@angular/core';
import { Transaction } from 'src/app/models/transaction.model';

@Component({
  selector: 'app-transaction-item',
  templateUrl: './transaction-item.component.html',
  styleUrls: ['./transaction-item.component.css']
})
export class TransactionItemComponent implements OnInit {

  constructor() { }
  @Input() transaction:Transaction;

  ngOnInit() {
  }

}
