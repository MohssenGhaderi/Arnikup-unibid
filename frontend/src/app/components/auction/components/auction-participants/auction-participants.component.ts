import { Component, OnInit, Input} from '@angular/core';
import { BaseAuction } from 'src/app/models/auction/baseAuction.model';
import { Links } from 'src/app/links.component';
import { LiveAuctionService } from 'src/app/services/live-auction.service';
import { States } from 'src/app/models/auction/states.model'


@Component({
  selector: 'app-auction-participants',
  templateUrl: './auction-participants.component.html',
  styleUrls: ['./auction-participants.component.css']
})
export class AuctionParticipantsComponent implements OnInit {
  @Input() auction: BaseAuction;
  Link = Links;
  listRendered = false;
  participants;
  states = new States();

  constructor(private auctionSocket:LiveAuctionService) {this.auctionSocket.connectToServer();}

  ngOnInit() {
    this.auctionSocket.users.subscribe(result =>{
      this.participants = result;
    });
    this.auctionSocket.states.subscribe(result=>{
      this.states = result;
    });
  }
  ngDoCheck(){
    if(!this.listRendered){
      if(this.auction && this.auction.participants){
        this.listRendered = true;
        this.participants = this.auction.participants;
      }
    }
  }


}
