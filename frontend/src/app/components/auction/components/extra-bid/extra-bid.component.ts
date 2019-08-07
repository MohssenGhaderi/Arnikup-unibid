import { Component, OnInit ,Input ,ViewChild, ElementRef } from '@angular/core';
import { SharingService } from 'src/app/services/sharing.service';
import { ExtraBids } from 'src/app/models/auction/extrabids.model';
import { MainServices } from 'src/app/services/main.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { ExtraBidMessage } from 'src/app/models/auction/extra-bid-message.model';

@Component({
  selector: 'app-extra-bid',
  templateUrl: './extra-bid.component.html',
  styleUrls: ['./extra-bid.component.css']
})
export class ExtraBidComponent implements OnInit {
  @Input() extraBids: ExtraBids;
  @Input() auctionId;
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;
  extraBidMessage = new ExtraBidMessage();

  constructor(private el:ElementRef,private shared:SharingService,private mainService:MainServices) {

  }

  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('details-auction-buy')[0].classList.add('myCfnAnimation-fadeIn');
  }

  closeExtrabid(){
    this.shared.extraBid = false;
    this.shared.extraBidUsed = true;
  }

  acceptExtraBids(eventData){
    eventData.preventDefault();
    this.loading.show();
    this.mainService.HandleExtraBid({"auctionId":this.auctionId}).subscribe(result=>{
      this.loading.hide();
      this.extraBidMessage.bids = result.bids;
      this.extraBidMessage.message = result.message;
      this.shared.emitExtraBidsChanged(this.extraBidMessage);
      this.shared.extraBidUsed = true;
      this.shared.extraBid = false;
    },
    error=>{
      this.loading.hide();
      this.shared.emitExtraBidsError(error.error.message);
      // .then(()=>{
        this.shared.extraBidUsed = true;
        this.shared.extraBid = false;
        // if(error.error.reason==="redirectShop"){
        //   this.shared.shop = true;
        // }
      // })
    });
  }

}
