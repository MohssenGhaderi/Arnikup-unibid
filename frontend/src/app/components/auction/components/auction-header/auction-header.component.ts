import { Component, OnInit, Input } from '@angular/core';
import { BaseAuction } from 'src/app/models/auction/baseAuction.model';

@Component({
  selector: 'app-auction-header',
  templateUrl: './auction-header.component.html',
  styleUrls: ['./auction-header.component.css']
})
export class AuctionHeaderComponent implements OnInit {
  @Input() auction: BaseAuction;

  constructor() { }

  ngOnInit() {
  }

}
