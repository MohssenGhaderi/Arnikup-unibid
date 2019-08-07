import { Component, OnInit, Input} from '@angular/core';
import { BaseAuction } from 'src/app/models/auction/baseAuction.model';
import { Links } from 'src/app/links.component';
import { LiveAuctionService } from 'src/app/services/live-auction.service';
import { States } from 'src/app/models/auction/states.model';


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
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.participants = result.users;
      }
    });

    this.auctionSocket.iceAge.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.states.iceAge = true;
        this.states.holliDay = false;
        this.states.hotSpot = false;
        this.states.feniTto = false;
        this.states.noWinner = false;
      }
    });

    this.auctionSocket.holliDay.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.states.iceAge = false;
        this.states.holliDay = true;
        this.states.hotSpot = false;
        this.states.feniTto = false;
        this.states.noWinner = false;
      }
    });

    this.auctionSocket.hotSpot.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.states.iceAge = false;
        this.states.holliDay = true;
        this.states.hotSpot = false;
        this.states.feniTto = false;
        this.states.noWinner = false;
      }
    });

    this.auctionSocket.winner.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.states.iceAge = false;
        this.states.holliDay = false;
        this.states.hotSpot = false;
        this.states.feniTto = true;
        this.states.noWinner = false;
      }
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
