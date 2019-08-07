import { Component, OnInit, ElementRef, Input} from '@angular/core';
import { SharingService } from 'src/app/services/sharing.service';
import { State } from 'src/app/models/user/information/state.model';
@Component({
  selector: 'app-small-states',
  templateUrl: './states.component.html',
  styleUrls: ['./states.component.css']
})
export class SmallStatesComponent implements OnInit {

  @Input() state:string;
  @Input() states:State[];
  selectedState:State;

  constructor(private el:ElementRef,private shared:SharingService) { }

  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('customDropdown')[0].classList.add('myCfnAnimation-swap-in');
  }
  goBack(){
    this.el.nativeElement.getElementsByClassName('customDropdown')[0].classList.add('myCfnAnimation-swap-out');
    setTimeout(()=>{
      this.shared.states = false;
    },500);
  }

  changeState(eventDate){
    this.state = eventDate.target.textContent;
    this.selectedState = this.states.find(x=>x.title==this.state);
    this.shared.emitState(this.selectedState);
    eventDate.stopPropagation();
    this.goBack();
  }

}
