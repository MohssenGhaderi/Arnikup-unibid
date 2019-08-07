import { Component, OnInit } from '@angular/core';
import { SharingService } from 'src/app/services/sharing.service';

@Component({
  selector: 'app-auto-bid',
  templateUrl: './auto-bid.component.html',
  styleUrls: ['./auto-bid.component.css']
})
export class AutoBidComponent implements OnInit {
  textValue;
  constructor(public shared:SharingService) {
    this.textValue = 5;
  }

  ngOnInit() {
  }

  toggleAutobid(){
    this.shared.autobid.state = !this.shared.autobid.state;
  }

  onDeadlineChange(value){
    this.shared.autobid.deadline = value;
  }
  showProductDetails(){
    this.shared.productDetails = true;
  }

}
