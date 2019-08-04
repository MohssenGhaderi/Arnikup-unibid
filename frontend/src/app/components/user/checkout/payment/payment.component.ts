import { Component, OnInit, ViewChild, ElementRef ,HostListener } from '@angular/core';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { UserService } from 'src/app/services/user.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { Links } from 'src/app/links.component';
import { Cart } from 'src/app/models/user/information/cart.model'

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
  totalPrice = 0;
  constructor(private el: ElementRef, private userService:UserService,private shared:SharingService,private liveUser:LiveUserService) { }

  @HostListener('mouseenter') onMouseEnter() {
    this.shared.visibleProfile = true;
  }
  @HostListener('mouseleave') onMouseLeave() {
    this.shared.visibleProfile = false;
  }

  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('paymentContainer')[0].classList.add(this.shared.basketClass);


    this.userSyncTimer = setInterval(() => {
      this.liveUser.getCarts();
    }, 1000);

    this.userService.GetShoppingCarts().subscribe(result => {
      this.carts = result;
      var costs = 0;
      var discounts = 0;
      this.carts.forEach(item =>{
        costs += item.price;
        discounts += item.discount;
      });
      this.totalPrice = costs - discounts;
      this.loading.hide();
    },
    error => {
      this.error.show(error,2000,'/signin');
    });

    this.liveUser.carts.subscribe(result=>{
      this.carts = result;
      var costs = 0;
      var discounts = 0;
      this.carts.forEach(item =>{
        costs += item.price;
        discounts += item.discount;
      });
      this.totalPrice = costs - discounts;
    });

  }

  goBack(){
    this.shared.basketClass = "myCfnAnimation-slideleft";
    this.shared.toggleMenu.payment = false;
    this.shared.toggleMenu.preview = true;
  }

}
