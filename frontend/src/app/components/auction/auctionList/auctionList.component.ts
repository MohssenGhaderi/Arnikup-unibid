import { Component, OnInit, ViewChild } from '@angular/core';
import { MainServices } from 'src/app/services/main.service';
import { GetAuctions } from 'src/app/models/service/getAuctions.model';
import { LoadingComponent } from 'src/app/components/loading/loading.component';

@Component({
  selector: 'app-auctionList',
  templateUrl: './auctionList.component.html',
  styleUrls: ['./auctionList.component.css']
})
export class AuctionListComponent implements OnInit {
  auctions: GetAuctions;

  items = [0,1,2,3,4,5];
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;

  constructor(private mainService: MainServices) { }

  ngOnInit() {
    this.loading.show();
    this.mainService.GetAuctions().subscribe(result => {
      this.auctions = result;
      this.loading.hide();
      this.items = [];
    },
    error => {
    });
  }

}
