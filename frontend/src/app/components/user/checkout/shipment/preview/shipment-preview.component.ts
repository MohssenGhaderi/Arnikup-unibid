import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { UserService } from 'src/app/services/user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { Links } from 'src/app/links.component';
import { Address } from 'src/app/models/user/information/address.model'

@Component({
  selector: 'app-shipment-preview',
  templateUrl: './shipment-preview.component.html',
  styleUrls: ['./shipment-preview.component.css']
})
export class ShipmentPreviewComponent implements OnInit {
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;
  address:Address;
  Link = Links;
  constructor(private el: ElementRef,private userService:UserService,private shared:SharingService) { }

  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('shipmentContainer')[0].classList.add(this.shared.basketClass);

    this.loading.show();
    this.userService.GetAddress().subscribe(result=>{
      this.loading.hide();
      this.address = result;
    },
    error=>{
      this.loading.hide();
      this.error.show(error,3000,'/signin');
    });
  }

  goBack(){
    this.shared.basketClass = "myCfnAnimation-slideleft";
    this.shared.toggleMenu.preview = false;
    this.shared.toggleMenu.shoppingCart = true;
  }

  goToNext(){
    this.shared.basketClass = "myCfnAnimation-slideright";
    this.shared.toggleMenu.preview = false;
    this.shared.toggleMenu.payment = true;
  }

  editAddress(eventData){
    eventData.preventDefault();
    this.shared.basketClass = "myCfnAnimation-slideright";
    this.shared.toggleMenu.preview = false;
    this.shared.toggleMenu.address = true;
  }

}
