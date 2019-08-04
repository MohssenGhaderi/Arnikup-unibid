import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { Auction } from 'src/app/models/auction/auction.model';
import { Links } from 'src/app/links.component';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';

@Component({
  selector: 'app-finished',
  templateUrl: './finished.component.html',
  styleUrls: ['./finished.component.css']
})
export class FinishedComponent implements OnInit {
  @Input() auction: Auction;
  Link = Links;
  toggleHeart = false;
  toggleSocial = false;
  @ViewChild(ErrorComponent ) error: ErrorComponent ;
  @ViewChild(SuccessComponent ) success: SuccessComponent ;
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;
  constructor(private service: MainServices,private shared:SharingService) { }

  ngOnInit() {
    this.toggleHeart = this.auction.liked;
  }

  closeSocial(){
    if(this.toggleSocial){
      this.shared.emitCloseSocial(this.auction.auctionId);
      setTimeout(()=>{
        this.toggleSocial = false;
      },1000);
    }else{
      this.toggleSocial = true;
    }
  }

  toggleClick(eventData, auctionId) {

      this.loading.show();
      this.service.likeAuction({auctionId:auctionId}).subscribe(result => {
        this.loading.hide();
        this.toggleHeart = !this.toggleHeart;
      },
      error => {
        this.loading.hide();
        this.error.show(error,2000,null);
      });
      eventData.stopPropagation();
    }

}
