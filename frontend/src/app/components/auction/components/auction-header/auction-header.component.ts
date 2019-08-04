import { Component, OnInit, Input } from '@angular/core';
import { BaseAuction } from 'src/app/models/auction/baseAuction.model';
import { SharingService } from 'src/app/services/sharing.service';


@Component({
  selector: 'app-auction-header',
  templateUrl: './auction-header.component.html',
  styleUrls: ['./auction-header.component.css']
})
export class AuctionHeaderComponent implements OnInit {
  @Input() auction: BaseAuction;
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
    console.log('pd');
    this.shared.productDetails = true;
  }

}
