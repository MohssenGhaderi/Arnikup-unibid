import { Component, OnInit, Input, ViewChild, EventEmitter, Output} from '@angular/core';
import { Cart } from 'src/app/models/user/information/cart.model';
import { UserService } from 'src/app/services/user.service';
import { Links } from 'src/app/links.component';
import { ItemGaranty } from 'src/app/models/itemGaranty.model';
import { SharingService } from 'src/app/services/sharing.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';

@Component({
  selector: 'app-cart-item',
  templateUrl: './cart-item.component.html',
  styleUrls: ['./cart-item.component.css']
})
export class CartItemComponent implements OnInit {
  @Input() cart:Cart;
  Link = Links;
  selectedGaranty = new ItemGaranty();
  toggleGaranty = false;
  subscription: any;
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;
  @Output() delete: EventEmitter<Cart> = new EventEmitter();

  constructor(private shared:SharingService,private userService:UserService) { }

  ngOnInit() {

    this.subscription = this.shared.getItemGarantyCloseEmitter().subscribe(result=>{
      if(result == this.cart.orderId){
        this.toggleGaranty = false;
      }

    });

    this.subscription = this.shared.getItemGarantyEmitter().subscribe(result=>{
      if(result.orderId == this.cart.orderId){
        this.selectedGaranty = result;
        this.toggleGaranty = false;
      }
    });
  }

  deleteOrder(eventData,orderId){
    eventData.preventDefault();
    this.loading.show();
    this.userService.DeleteOrder({"orderId":orderId}).subscribe(result=>{
      this.loading.hide();
      this.success.show(result,2000).then(()=>{
        this.delete.emit(this.cart);
      });
    },
    error => {
      this.loading.hide();
      this.error.show(error,3000);
    });
  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
  }

}
