import { Component, OnInit ,Input, ElementRef } from '@angular/core';
import { Cart } from 'src/app/models/cart.model';
import { Details } from 'src/app/models/details.model';
import { AuctionPlan } from 'src/app/models/auction/auctionPlan.model';
import { SharingService } from 'src/app/services/sharing.service';

@Component({
  selector: 'app-participated',
  templateUrl: './participated.component.html',
  styleUrls: ['./participated.component.css']
})
export class ParticipatedComponent implements OnInit {
  @Input() auctionId: number;
  @Input() auctionTitle: string;
  @Input() details:Details;
  @Input() plan:AuctionPlan;
  cart = new Cart();
  constructor(private el: ElementRef,private shared:SharingService) {
  }

  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('registerAuction')[0].classList.add('cfnAnimation-slideup');
  }

  close(eventData){
    this.el.nativeElement.getElementsByClassName('registerAuction')[0].classList.add('cfnAnimation-slidedown');
    setTimeout(()=>{
      this.cart.auctionId = this.auctionId;
      this.cart.state = "closed";
      this.cart.participated = true;
      if(this.details){
        this.cart.details = this.details;
      }
      this.shared.emitCartState(this.cart);
    },1000);
    eventData.stopPropagation();
  }
}
