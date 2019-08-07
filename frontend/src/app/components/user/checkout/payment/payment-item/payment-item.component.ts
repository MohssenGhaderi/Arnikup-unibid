import { Component, OnInit, Input } from '@angular/core';
import { Cart } from 'src/app/models/user/information/cart.model';
import { ItemGaranty } from 'src/app/models/itemGaranty.model';
import { SharingService } from 'src/app/services/sharing.service';

@Component({
  selector: 'app-payment-item',
  templateUrl: './payment-item.component.html',
  styleUrls: ['./payment-item.component.css']
})
export class PaymentItemComponent implements OnInit {
  @Input() cart:Cart;
  selectedGaranty = new ItemGaranty();
  totalPrice:number;

  constructor(private shared:SharingService) { }

  ngOnInit() {
    if(this.shared.checkoutInfo){
      if(this.shared.checkoutInfo.garanties)
        this.shared.checkoutInfo.garanties.forEach(item=>{
          if(item.garantyId!=0 && this.cart.orderId==item.orderId)
            this.selectedGaranty = item;
        });
    }
  }
}
