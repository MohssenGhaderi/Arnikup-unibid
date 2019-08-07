import { Component, OnInit, ElementRef, Input} from '@angular/core';
import { SharingService } from 'src/app/services/sharing.service';
import { ShipmentMethod } from 'src/app/models/shipmentMethod.model';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-shipment-method',
  templateUrl: './shipment-method.component.html',
  styleUrls: ['./shipment-method.component.css']
})
export class ShipmentMethodComponent implements OnInit {
  @Input() method:string;
  @Input() methods:ShipmentMethod[];
  selectedMethod = new ShipmentMethod();

  constructor(private el:ElementRef,private shared:SharingService,private service:UserService) { }

  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('customDropdown')[0].classList.add('myCfnAnimation-swap-in');
  }

  goBack(){

  }

  changeMethod(eventDate,methodId){
    this.method = eventDate.target.textContent;
    this.selectedMethod = this.methods.find(x=>x.methodId==methodId);
    eventDate.stopPropagation();
    this.el.nativeElement.getElementsByClassName('customDropdown')[0].classList.add('myCfnAnimation-swap-out');
    this.shared.emitShipmentMethod(this.selectedMethod);
  }
}
