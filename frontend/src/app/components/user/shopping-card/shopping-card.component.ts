import { Component, OnInit, ViewChild, ElementRef, HostListener } from '@angular/core';
import { UserService } from 'src/app/services/user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { Cart } from 'src/app/models/user/information/cart.model'
import { Links } from 'src/app/links.component';
import { ShipmentMethod } from 'src/app/models/shipmentMethod.model';
import { ItemGaranty } from 'src/app/models/itemGaranty.model';

@Component({
  selector: 'app-shopping-card',
  templateUrl: './shopping-card.component.html',
  styleUrls: ['./shopping-card.component.css']
})
export class ShoppingCardComponent implements OnInit {

  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;

  Link = Links;
  userSyncTimer;
  carts:Cart[];
  toggleShipmentMethod = false;
  selectedMethod = new ShipmentMethod();
  selectedGaranty = new ItemGaranty();
  methods;
  garanties:Array<ItemGaranty>;
  subscription: any;
  totalPrice;

  constructor(private el: ElementRef, private userService:UserService,private shared:SharingService,private liveUser:LiveUserService) { }

  @HostListener('mouseenter') onMouseEnter() {
    this.shared.visibleProfile = true;
  }
  @HostListener('mouseleave') onMouseLeave() {
    this.shared.visibleProfile = false;
  }

  ngOnInit() {
    this.garanties = this.shared.checkoutInfo.garanties;

    this.subscription = this.shared.getShipmentMethodEmitter().subscribe(result=>{
      this.selectedMethod = result;
      this.toggleShipmentMethod = false;
      this.shared.checkoutInfo.method = result;
    });

    this.subscription = this.shared.getItemGarantyEmitter().subscribe(result=>{
      this.garanties = this.garanties.filter(function(value, index, arr){
          return value.orderId!=result.orderId;
      });
      this.garanties.push(result);
      this.shared.checkoutInfo.garanties = this.garanties;
      this.updatePrices();
    });

    this.el.nativeElement.getElementsByClassName('profileContainer')[0].classList.add(this.shared.basketClass);

    this.userService.GetShoppingCarts().subscribe(result => {
      this.carts = result;

      this.userService.GetShipmentMethods().subscribe(result => {

        this.methods = result;
        this.updatePrices();

        this.shared.checkoutInfo.garanties.forEach(garanty=>{
          setTimeout(()=>{
            this.shared.emitItemGaranty(garanty);
          },500);
        });

        if(this.shared.checkoutInfo.method)
          this.shared.emitShipmentMethod(this.shared.checkoutInfo.method);

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
     this.totalPrice = costs - discounts;
   }

  goBack(){
    this.shared.lastClass = "myCfnAnimation-slideup";
    this.shared.basketClass = "myCfnAnimation-slideright";
    this.shared.toggleMenu.profile = true;
    this.shared.toggleMenu.shoppingCart = false;
  }

  togglePreview(){
    if(this.totalPrice>0){
      this.shared.toggleMenu.reset();
      this.shared.basketClass = "myCfnAnimation-slideright";
      this.shared.toggleMenu.preview = true;
    }
  }

  toggleShipmentMenu(){
    this.shared.shipmentMethod = !this.shared.shipmentMethod;
  }

  deleteCart(cart: Cart) {
    this.shared.checkoutInfo.garanties = this.shared.checkoutInfo.garanties.filter(x => x.orderId != cart.orderId);
    this.carts = this.carts.filter(x => x.orderId != cart.orderId);
    if(this.carts.length==0)
      this.shared.checkoutInfo.method = null;
    this.updatePrices();
  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
  }

}
