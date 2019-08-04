import { Component, OnInit ,Input ,ViewChild, ElementRef } from '@angular/core';
import { LoadingComponent } from 'src/app/components/loading/loading.component'
import { ErrorComponent } from 'src/app/components/error/error.component'
import { SuccessComponent } from 'src/app/components/success/success.component'
import { Coin } from 'src/app/models/auction/coin.model';
import { Cart } from 'src/app/models/cart.model';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { Details } from 'src/app/models/details.model'
@Component({
  selector: 'app-coin-participate',
  templateUrl: './coin-participate.component.html',
  styleUrls: ['./coin-participate.component.css']
})
export class CoinParticipateComponent implements OnInit {
  @Input() coins: Coin[];
  @Input() auctionId: number;
  @ViewChild(ErrorComponent ) error: ErrorComponent ;
  @ViewChild(SuccessComponent ) success: SuccessComponent ;
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;
  cart = new Cart();

  constructor(private el: ElementRef, private service: MainServices,private shared:SharingService) {
  }

  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('registerAuction')[0].classList.add('cfnAnimation-slideup');
  }
  ngAfterViewInit(){
    this.cart.auctionId = this.auctionId;
  }

  close(eventData){
    eventData.stopPropagation();
    this.el.nativeElement.getElementsByClassName('registerAuction')[0].classList.add('cfnAnimation-slidedown');
    setTimeout(()=>{
      this.cart.state = "closed";
      this.shared.emitCartState(this.cart);
    },1000);
  }

  stopEvent(eventData){
    eventData.stopPropagation();
  }

  registerByCoin(eventData,auctionId,planId){
    this.loading.show();
    this.service.registerByCoin({auctionId:auctionId,planId:planId}).subscribe(result => {
      this.loading.hide();
      this.success.show(result,2000).then(()=>{
        this.el.nativeElement.getElementsByClassName('registerAuction')[0].classList.add('cfnAnimation-slidedown');
        this.cart.details = result.details;
        this.cart.state = "confirmed";
        this.cart.participated = true;
        this.shared.emitCartState(this.cart);
      });
    },
    error => {
      this.loading.hide();
      this.error.show(error,1500,null).then(()=>{
        setTimeout(()=>{
          if(error.error.reason==="coins"){
            this.el.nativeElement.getElementsByClassName('registerAuction')[0].classList.add('cfnAnimation-slidedown-none');
            this.cart.details = error.error.details;
            this.cart.state = "gems";
            this.cart.participated = false;
            this.shared.emitCartState(this.cart);
          }
        },500);
      });
    });
    eventData.stopPropagation();
  }

}
