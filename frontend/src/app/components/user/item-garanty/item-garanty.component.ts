import { Component, OnInit, ElementRef, Input} from '@angular/core';
import { SharingService } from 'src/app/services/sharing.service';
import { ItemGaranty } from 'src/app/models/itemGaranty.model';

@Component({
  selector: 'app-item-garanty',
  templateUrl: './item-garanty.component.html',
  styleUrls: ['./item-garanty.component.css']
})
export class ItemGarantyComponent implements OnInit {
  @Input() garanty:string;
  @Input() garanties:ItemGaranty[];
  @Input() orderId:number;

  selectedGaranty = new ItemGaranty();

  constructor(private el:ElementRef,private shared:SharingService) { }

  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('customDropdown')[0].classList.add('myCfnAnimation-swap-in');
  }

  goBack(){

  }

  changeGaranty(eventDate,garantyId){
    eventDate.stopPropagation();
    this.garanty = eventDate.target.textContent;
    this.selectedGaranty = this.garanties.find(x=>x.garantyId===garantyId);
    this.shared.emitItemGaranty(this.selectedGaranty);
    this.el.nativeElement.getElementsByClassName('customDropdown')[0].classList.add('myCfnAnimation-swap-out');
    this.shared.emitItemGarantyClose(this.orderId);
  }


}
