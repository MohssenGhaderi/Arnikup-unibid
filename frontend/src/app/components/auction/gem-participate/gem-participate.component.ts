import { Component, OnInit ,Input ,ViewChild, ElementRef } from '@angular/core';
import { LoadingComponent } from 'src/app/components/loading/loading.component'
import { ErrorComponent } from 'src/app/components/error/error.component'
import { SuccessComponent } from 'src/app/components/success/success.component'
import { Coin } from 'src/app/models/auction/coin.model';
import { Cart } from 'src/app/models/cart.model';
import { Details } from 'src/app/models/details.model';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';

@Component({
  selector: 'app-gem-participate',
  templateUrl: './gem-participate.component.html',
  styleUrls: ['./gem-participate.component.css']
})
export class GemParticipateComponent implements OnInit {
  @Input() coins: Coin[];
  @Input() auctionId: number;
  @Input() planId: number;
  @Input() details:Details;
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
    this.el.nativeElement.getElementsByClassName('registerAuction')[0].classList.add('cfnAnimation-slidedown');
    setTimeout(()=>{
      this.cart.auctionId = this.auctionId;
      this.cart.state = "closed";
      this.shared.emitCartState(this.cart);
    },1000);
    eventData.stopPropagation();
  }

  registerByGem(eventData){
    this.loading.show();
    this.service.registerByGem({auctionId:this.auctionId,planId:this.details.planId}).subscribe(result => {
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
      if(error.error.reason=="redirectShop"){
        this.error.show(error,2000,null)
        .then(()=>{
          this.shared.shop = true;
        });
      }else{
        this.error.show(error,2000,null);
      }
    });
    eventData.stopPropagation();
  }
}
