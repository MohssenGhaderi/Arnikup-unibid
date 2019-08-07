import { Component, OnInit, ViewChild } from '@angular/core';
import { MainServices } from 'src/app/services/main.service';
import { GetAuctions } from 'src/app/models/service/getAuctions.model';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { SharingService } from 'src/app/services/sharing.service';


@Component({
  selector: 'app-auctionList',
  templateUrl: './auctionList.component.html',
  styleUrls: ['./auctionList.component.css']
})
export class AuctionListComponent implements OnInit {
  auctions: GetAuctions;
  subscription: any;
  items = [0,1,2,3,4,5];

  @ViewChild(LoadingComponent ) loading: LoadingComponent ;

  constructor(private mainService: MainServices,private shared:SharingService) { }

  ngOnInit() {
    this.subscription = this.shared.getScrollReachedEmitter().subscribe(result=>{
      this.items = [0,1,2,3,4,5];
      var searchObj = {"start":this.auctions.lastAuctions.length,"stop":this.auctions.lastAuctions.length+6};

      this.mainService.GetAuctionsLazy(searchObj).subscribe(result => {
        result.lastAuctions.forEach(item=>{
          this.auctions.lastAuctions.push(item);
        })
        this.loading.hide();
        this.items = [];
        this.shared.auctions += result.lastAuctions.length;
        this.shared.busyScroll = this.auctions.lastAuctions.length==this.shared.allAuctions ;
      },
      error => {
      });


    });

    this.loading.show();
    this.mainService.GetAuctions().subscribe(result => {
      this.auctions = result;
      this.shared.auctions = result.lastAuctions.length;
      this.shared.allAuctions = result.total;
      this.loading.hide();
      this.items = [];
    },
    error => {
    });
  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
  }


}
