import { Component, OnInit, ElementRef, Input} from '@angular/core';
import { SharingService } from 'src/app/services/sharing.service';
import { State } from 'src/app/models/user/information/state.model';

@Component({
  selector: 'app-message-type',
  templateUrl: './message-type.component.html',
  styleUrls: ['./message-type.component.css']
})
export class MessageTypeComponent implements OnInit {

  @Input() messageType :string;
  constructor(private el:ElementRef,private shared:SharingService) { }

  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('customDropdown')[0].classList.add('myCfnAnimation-swap-in');
  }
  goBack(){
    this.el.nativeElement.getElementsByClassName('customDropdown')[0].classList.add('myCfnAnimation-swap-out');
    setTimeout(()=>{
      this.shared.emitCloseMessageType(this.messageType);
    },200);
  }

  changeState(eventDate){
    this.messageType = eventDate.target.textContent;
    eventDate.stopPropagation();
    this.goBack();
  }

}
