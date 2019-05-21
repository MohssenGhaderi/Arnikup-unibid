import { Component, OnInit } from '@angular/core';
import { MainServices } from 'src/app/_services/main.service';
import { GetAuctions } from 'src/app/models/service/getAuctions.model';

@Component({
  selector: 'app-auctionList',
  templateUrl: './auctionList.component.html',
  styleUrls: ['./auctionList.component.css']
})
export class AuctionListComponent implements OnInit {
  auctions: GetAuctions;
  loading = true;
  constructor(private mainService: MainServices) { }

  ngOnInit() {
    this.mainService.GetAuctions().subscribe(result => {
      this.auctions = result;
      this.loading = false;
    },
    error => {
    });
  }

}
