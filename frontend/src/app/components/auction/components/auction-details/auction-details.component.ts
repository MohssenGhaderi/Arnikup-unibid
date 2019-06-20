import { Component, OnInit ,Input ,ViewChild ,ElementRef } from '@angular/core';
import { BaseAuction } from 'src/app/models/auction/baseAuction.model';
import { LiveAuctionService } from 'src/app/services/live-auction.service';
import { ProgressComponent } from 'src/app/components/progress/progress.component';
import { Router } from '@angular/router';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { Links } from 'src/app/links.component';
import { States } from 'src/app/models/auction/states.model';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';

@Component({
  selector: 'app-auction-details',
  templateUrl: './auction-details.component.html',
  styleUrls: ['./auction-details.component.css']
})
export class AuctionDetailsComponent implements OnInit {
  @Input() auction: BaseAuction;
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;
  @ViewChild(ProgressComponent ) progress: ProgressComponent ;

  remainedTime;
  timer;
  timeoutId;
  auctionTimer;
  joined = false;
  Link = Links;
  states = new States();

  constructor(
    private auctionSocket:LiveAuctionService,
    private router:Router,
    private authService:AuthenticationService
  )
  {this.auctionSocket.connectToServer();}

  ngOnInit() {
    console.log(this.states);
  }
  ngDoCheck(){

    if (this.auction) {

      // client timer
      if(!this.timer){
        this.remainedTime = this.ConvertMS(this.auction.remainedTime);
        this.timer = setInterval(() => {
          this.auction.remainedTime -= 1000;
          this.remainedTime = this.ConvertMS(this.auction.remainedTime);
        }, 1000);
      }

      // get live auction status
      if(this.states.iceAge && !this.auctionTimer){
        this.auctionTimer = setInterval(() => {
          console.log('getAuction status');
          this.auctionSocket.getAuction(this.auction.auctionId);
        }, 1000);
      }

      // join client to the auctions room
      if(this.states.holliDay && !this.joined){
        clearInterval(this.auctionTimer);
        this.loading.show();
        this.joined = true;
        this.auctionSocket.join(this.auction.auctionId);
      }
    }
  }
  ngAfterViewInit(){
    this.auctionSocket.connect.subscribe(result => console.log(result));

    this.auctionSocket.joined.subscribe(result => {
      console.log(result);
      this.auctionSocket.getStatus(this.auction.auctionId);
      this.loading.hide();
    });

    this.auctionSocket.bids.subscribe(result => {
      this.auction.bids = parseInt(result);
      this.loading.hide();
    });

    this.auctionSocket.accepted.subscribe(result => {
      var remainingTime = parseInt(result);
      this.auction.remainedTime = remainingTime;
      if (this.states.hotSpot){
        this.progress.reset();
      }
      this.auctionSocket.getStatus(this.auction.auctionId);
      this.auctionSocket.getUsers(this.auction.auctionId);
      this.loading.hide();
    });

    this.auctionSocket.remained.subscribe(result => {

      console.log('continue');
      this.auction.remainedTime = parseInt(result);
      this.loading.hide();

    });

    this.auctionSocket.winner.subscribe(result => {

      console.log('done');
      this.auction.status = result;
      this.loading.hide();
      this.auction.done = true;

    });

    this.auctionSocket.done.subscribe(result => {
      console.log(result);
      this.loading.hide();
      // this.auction.done = true;
      // this.auctionSocket.disconnect();
    });

    this.auctionSocket.states.subscribe(result=>{
      this.states = result;
      if(this.states.feniTto){
        this.loading.show();
      }
      // console.log(this.states);
    });



    this.auctionSocket.failed.subscribe(result => {
      this.loading.hide();
      this.error.show(result,2000,null);
    });

  }

  handleBid(eventData,auctionId){
    console.log('try bid for : ',auctionId);

    this.auctionSocket.offerBid(auctionId);

    eventData.stopPropagation();
  }

  ngOnDestroy(){
    this.auctionSocket.disconnect();
    clearInterval(this.timer);
  }

  tryParseInt(number){
    return parseInt(Math.floor(number).toString());
  }

  ConvertMS(ms) {
    let day,
        hour,
        minute,
        seconds;
    seconds = Math.floor(ms / 1000);
    minute = Math.floor(seconds / 60);
    seconds = seconds % 60;
    hour = Math.floor(minute / 60);
    minute = minute % 60;
    day = Math.floor(hour / 24);
    hour = hour % 24;
    return {
        day: day,
        hour: hour,
        minute: minute,
        seconds: seconds
    };
  }

}
