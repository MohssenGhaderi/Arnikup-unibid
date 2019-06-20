import { Component, OnInit, Input, ViewChild, ElementRef ,ViewChildren, QueryList} from '@angular/core';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { Auction } from 'src/app/models/auction.model';
import { Links } from 'src/app/links.component';
import { Router } from '@angular/router';
import { GetParticipation } from 'src/app/models/getParticipation.model';
import { LiveAuctionService } from 'src/app/services/live-auction.service';
import { ProgressComponent } from 'src/app/components/progress/progress.component';
import { AuctionStatus } from 'src/app/models/auctionStatus.model';
import { LoadingComponent } from 'src/app/components/loading/loading.component'
import { ErrorComponent } from 'src/app/components/error/error.component'
import { SuccessComponent } from 'src/app/components/success/success.component'

@Component({
  selector: 'app-auctionItem',
  templateUrl: './auctionItem.component.html',
  styleUrls: ['./auctionItem.component.css']
})

export class AuctionItemComponent implements OnInit {
  toggleHeart = false;
  showRegisterAuction = false;
  hideRegisterAuction = false;
  coinState = 'pallet';
  GetParticipation = GetParticipation;
  participated = false;
  Link = Links;
  remainedTime;
  timer;
  joined = false;
  timeoutId = 0;

  @Input() auction: Auction;
  @ViewChild('errorMessage') errorMessageElem: ElementRef;
  @ViewChild(ProgressComponent ) progress: ProgressComponent ;
  @ViewChild(ErrorComponent ) error: ErrorComponent ;
  @ViewChild(SuccessComponent ) success: SuccessComponent ;
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;

  currentTime = Math.floor(Math.random() * (10 - 4)) + 4;
  totalSegments = 10 ;

  constructor(
    private service: MainServices,
    private authService:AuthenticationService,
    private router: Router,
    private auctionSocket:LiveAuctionService,
    private shared:SharingService,
  )
  {this.auctionSocket.connectToServer();}

  ngOnInit() {
    // this.auctionSocket.connect();
    // this.auctionSubscription = this.auctionSocket.connect.pipe().subscribe(result => console.log(result));
    this.toggleHeart = this.auction.liked;

    if (this.auction) {
      this.remainedTime = this.ConvertMS(this.auction.remainedTime);
      this.timer = setInterval(() => {
        this.auction.remainedTime = this.auction.remainedTime - 1000;
        this.remainedTime = this.ConvertMS(this.auction.remainedTime);
      }, 1000);
    }

  }

  ngDoCheck(){
    // this.auction.started = new StartedAuction();
    if(this.auction.remainedTime <= 60000 && !this.joined){
      this.joined = true;
      this.auctionSocket.join(this.auction.auctionId);
    }

  }

  ngOnDestroy() {
    // this.auctionSubscription.unsubscribe();
    this.auctionSocket.disconnect();
    clearInterval(this.timer);
  }

  ngAfterViewInit() {

    this.auctionSocket.connect.subscribe(result => console.log(result));

    this.auctionSocket.joined.subscribe(result => {
      console.log(result);
      this.auctionSocket.getStatus(this.auction.auctionId);
    });

    this.auctionSocket.bids.subscribe(result => {
      this.auction.bids = parseInt(result);
    });

    this.auctionSocket.accepted.subscribe(result => {
      var remainingTime = parseInt(result);
      this.auction.remainedTime = remainingTime;
      if (this.auction.remainedTime <= 11000){
        this.progress.reset();
      }
      this.auctionSocket.getStatus(this.auction.auctionId);
    });

    this.auctionSocket.status.subscribe(result => {
      console.log(result);
      this.auction.status = result;
    });

    this.auctionSocket.failed.subscribe(result => {
      this.loading.hide();
      this.error.show(result,2000,null);
    });

  }

  tryParseInt(number){
    return parseInt(Math.floor(number).toString());
  }

  handleBid(eventData,auctionId){
    console.log('try bid for : ',auctionId);

    this.auctionSocket.offerBid(auctionId);

    eventData.stopPropagation();
  }

  toggleClick(eventData, auctionId) {

      this.loading.show();
      this.service.likeAuction({auctionId:auctionId}).subscribe(result => {
        this.toggleHeart = !this.toggleHeart;
        this.loading.hide();
      },
      error => {
        this.loading.hide();
        this.error.show(error,2000,null);
      });
      eventData.stopPropagation();
    }

  RegisterAuctionSlideupClick() {
    this.showRegisterAuction = true;
  }

  RegisterAuctionSlideDownClick(eventData) {
    this.hideRegisterAuction = true;
    setTimeout(() => {
      // this.coinState = 'pallet';
      this.showRegisterAuction = false;
      this.hideRegisterAuction = false;
    }, 1000);
    eventData.stopPropagation();
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

  registerByCoin(eventData,auctionId,planId){
    this.loading.show();
    this.service.registerByCoin({auctionId:auctionId,planId:planId}).subscribe(result => {
      this.loading.hide();
      this.GetParticipation = <any>result;
      this.coinState = 'confirmed';
      this.participated = true;
    },
    error => {
      if(error.error.reason==="coins"){
        this.GetParticipation = error.error;
        this.coinState = 'gems';
      }
      this.loading.hide();
      this.error.show(error,2000,null);
    });
    eventData.stopPropagation();
  }

  registerByGem(eventData,auctionId,planId){
    eventData.stopPropagation();

    this.loading.show();
    this.service.registerByGem({auctionId:auctionId,planId:planId}).subscribe(result => {
      this.loading.hide();
      this.GetParticipation = <any>result;
      this.coinState = 'confirmed';
      this.participated = true;
    },
    error => {
      if(error.error.reason==="coins"){
        this.GetParticipation = error.error;
        this.coinState = 'gems';
      }

      this.loading.hide();

      if(error.error.reason=="redirectShop"){
        this.error.show(error,2000,null)
        .then(()=>{
          this.shared.shop = true;
        });
      }else{
        this.error.show(error,2000,null);
      }
    });

  }
}
