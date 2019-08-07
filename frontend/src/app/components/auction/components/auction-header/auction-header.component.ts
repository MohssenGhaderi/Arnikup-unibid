import { Component, OnInit, Input } from '@angular/core';
import { BaseAuction } from 'src/app/models/auction/baseAuction.model';
import { SharingService } from 'src/app/services/sharing.service';
import { Links } from 'src/app/links.component';

@Component({
  selector: 'app-auction-header',
  templateUrl: './auction-header.component.html',
  styleUrls: ['./auction-header.component.css']
})
export class AuctionHeaderComponent implements OnInit {
  @Input() auction: BaseAuction;
  Link = Links;

  constructor(public shared:SharingService) {}
  subscription: any;
  toggleSocial = false;
  ngOnInit() {
    this.subscription = this.shared.getSocialStayEmitter().subscribe((auctionId)=>{
      if(this.auction.auctionId==auctionId){
        setTimeout(()=>{
          this.toggleSocial = false;
        },300);
      }
    });
  }
  closeOpenedSocial(eventData){
    if(this.toggleSocial){
      this.shared.emitCloseSocial(this.auction.auctionId);
    }
    eventData.stopPropagation();
  }
  showProductDetails(){
    this.shared.productDetails = true;
  }
  closeSocial(eventData){
    if(this.toggleSocial){
      this.shared.emitCloseSocial(this.auction.auctionId);
      setTimeout(()=>{
        this.toggleSocial = false;
      },300);
    }else{
      this.toggleSocial = true;
    }
    eventData.stopPropagation();
  }
}
