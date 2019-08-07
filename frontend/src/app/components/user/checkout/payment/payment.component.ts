import { Component, OnInit, ViewChild, ElementRef ,HostListener } from '@angular/core';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { UserService } from 'src/app/services/user.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { Links } from 'src/app/links.component';
import { Cart } from 'src/app/models/user/information/cart.model';
import { UserCoupon } from 'src/app/models/user/userCoupon.model';
import { Buy } from 'src/app/models/shop/buy.model';
import { PaymentServices } from 'src/app/services/payment.service';
import { ShipmentMethod } from 'src/app/models/shipmentMethod.model';
import { ItemGaranty } from 'src/app/models/itemGaranty.model';

@Component({
  selector: 'app-payment',
  templateUrl: './payment.component.html',
  styleUrls: ['./payment.component.css']
})
export class PaymentComponent implements OnInit {
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;

  Link = Links;
  userSyncTimer;
  carts:Cart[];
  userCoupon:UserCoupon;
  subscription: any;
  buy = new Buy();
  selectedMethod = new ShipmentMethod();
  totalPrice;

  constructor(
    private el: ElementRef,
    private userService:UserService,
    public shared:SharingService,
    private liveUser:LiveUserService,
    private service: PaymentServices
  ) { }

  @HostListener('mouseenter') onMouseEnter() {
    this.shared.visibleProfile = true;
  }
  @HostListener('mouseleave') onMouseLeave() {
    this.shared.visibleProfile = false;
  }

  ngOnInit() {

    this.subscription = this.shared.getCouponEmitter().subscribe(result=>{
      this.userCoupon = result;
    });

    this.el.nativeElement.getElementsByClassName('paymentContainer')[0].classList.add(this.shared.basketClass);

    this.userService.GetShoppingCarts().subscribe(result => {
      this.carts = result;
      this.userService.GetUserCoupon().subscribe(result=>{
        this.userCoupon = result;
        this.updatePrices();
      },
      error=>{
        this.error.show(error,2000);
      });
      this.loading.hide();
    },
    error => {
      this.error.show(error,2000,'/signin');
    });

  }

  updatePrices(){

    var costs = 0;
    var discounts = 0;
    if(this.carts){
      this.carts.forEach(item =>{
        costs += parseInt(item.price.toString());
        discounts += parseInt(item.discount.toString());
      });
    }
    if(this.shared.checkoutInfo.garanties){
      this.shared.checkoutInfo.garanties.forEach(garanty=>{
          costs += garanty.price;
      });

      if(this.shared.checkoutInfo.method)
       costs += this.shared.checkoutInfo.method.price;
    }
    if(this.userCoupon){

      discounts += parseInt(this.userCoupon.amount.toString());
    }
    this.totalPrice = costs - discounts;
  }



  goBack(){
    this.shared.basketClass = "myCfnAnimation-slideleft";
    this.shared.toggleMenu.payment = false;
    this.shared.toggleMenu.preview = true;
  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
  }

  buyProduct(){

      this.loading.show();
      this.service.BuyProduct().subscribe(result=>{
        this.success.show(result,1000).then(()=>{
          this.service.PaymentGateway({"GUID":result.GUID}).subscribe(pay=>{
            console.log(pay);
            console.log('redirect to bank');
          },
          error=>{
            this.loading.hide();
            this.error.show(error,3000,null);
          });
        });
      },
      error =>{
        this.loading.hide();
        this.error.show(error,3000,null);
      });

  }

}
