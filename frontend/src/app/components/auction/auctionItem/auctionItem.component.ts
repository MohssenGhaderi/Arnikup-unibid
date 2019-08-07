import { Component, OnInit, Input, ViewChild, ElementRef ,ViewChildren, QueryList} from '@angular/core';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { Auction } from 'src/app/models/auction/auction.model';
import { Links } from 'src/app/links.component';
import { Router } from '@angular/router';
import { GetParticipation } from 'src/app/models/auction/getParticipation.model';
import { LiveAuctionService } from 'src/app/services/live-auction.service';
import { ProgressComponent } from 'src/app/components/progress/progress.component';
import { AuctionStatus } from 'src/app/models/auction/auctionStatus.model';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { Cart } from 'src/app/models/cart.model';
import { Joined } from 'src/app/models/socket/joined.model';

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
  cart:Cart;
  joined = false;

  timeoutId = 0;
  subscription: any;
  toggleSocial = false;

  @Input() auction: Auction;
  @ViewChild(ProgressComponent ) progress: ProgressComponent ;
  @ViewChild(ErrorComponent ) error: ErrorComponent ;
  @ViewChild(SuccessComponent ) success: SuccessComponent ;
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;

  currentTime = Math.floor(Math.random() * (10 - 4)) + 4;
  totalSegments = 10 ;

  constructor(
    private el:ElementRef,
    private service: MainServices,
    private authService:AuthenticationService,
    private router: Router,
    private auctionSocket:LiveAuctionService,
    private shared:SharingService,
  )
  {
    this.auctionSocket.connectToServer();
    this.cart = new Cart();

  }

  ngOnInit() {

    if(!this.timer){
      this.remainedTime = this.ConvertMS(this.auction.remainedTime);
      this.timer = setInterval(() => {
        this.auction.remainedTime = this.auction.remainedTime - 1000;
        this.remainedTime = this.ConvertMS(this.auction.remainedTime);
      }, 1000);
    }

    this.cart.auctionId = this.auction.auctionId;
    this.toggleHeart = this.auction.liked;

    this.subscription = this.shared.getCartStateEmitter().subscribe(result=>{
      if(this.auction.auctionId == result.auctionId){
        this.cart.state = result.state;
        this.cart.details = result.details;
        this.cart.participated = result.participated;
        if (result.scroll)
          this.el.nativeElement.scrollIntoView();
      }
    });

    this.subscription = this.shared.getSocialStayEmitter().subscribe((auctionId)=>{
      if(this.auction.auctionId==auctionId){
        setTimeout(()=>{
          this.toggleSocial = false;
        },1000);
      }
    });

    this.auctionSocket.connect.subscribe(result => console.log(result));

    this.auctionSocket.iceAge.subscribe(result =>{
      if(this.auction.auctionId===result.auctionId){
        this.auction.remainedTime = result.heartbeat;
        if(!this.timer){
          this.remainedTime = this.ConvertMS(this.auction.remainedTime);
          this.timer = setInterval(() => {
            this.auction.remainedTime = this.auction.remainedTime - 1000;
            this.remainedTime = this.ConvertMS(this.auction.remainedTime);
          }, 1000);
        }
      }
    });

    this.auctionSocket.holliDay.subscribe(result =>{
      if(this.auction.auctionId===result.auctionId){
        this.auction.remainedTime = result.heartbeat;
        if(!this.joined){
          this.joined = true;
          this.auctionSocket.PublicRoom(this.auction.auctionId);
          this.auctionSocket.PrivateRoom(this.auction.auctionId);
        }
      }
    });

    this.auctionSocket.joined.subscribe(result => {
      if(this.auction.auctionId===result.auctionId){
        this.auctionSocket.getStatus(this.auction.auctionId);
      }
    });

    this.auctionSocket.status.subscribe(result => {
      if(this.auction.auctionId===result.auctionId){
        this.auction.status = result.status;
      }
    });

    this.auctionSocket.bids.subscribe(result => {
      if(this.auction.auctionId===result.auctionId){
        this.auction.bids = result.bids;
        this.auctionSocket.getUsers(this.auction.auctionId);
        this.loading.hide();
      }
    });

    this.auctionSocket.reset.subscribe(result => {
      if(this.auction.auctionId===result.auctionId){
        this.auction.remainedTime = result.heartbeat;
        this.progress.reset(10,10);
        this.loading.hide();
      }
    });

    this.auctionSocket.winner.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.auction.status = result.winner;
        this.success.show({"message":"حراجی با موفقیت به اتمام رسید"},2000).then(()=>{
          this.loading.hide();
        })
      }
    });

    this.auctionSocket.zeroTime.subscribe(result => {

      if(this.auction.auctionId===result.auctionId){
        this.success.show(result,2000);
      }
    });

    this.auctionSocket.feniTto.subscribe(result => {
      if(this.auction.auctionId===result.auctionId){
        this.error.show(result,2000);
      }
    });

    this.auctionSocket.failed.subscribe(result => {
      if(this.auction.auctionId===result.error.auctionId){
        this.loading.hide();
        this.error.show(result,2000,null);
      }
    });

  }

  closeSocial(eventData){
    if(this.toggleSocial){
      this.shared.emitCloseSocial(this.auction.auctionId);
      setTimeout(()=>{
        this.toggleSocial = false;
      },1000);
    }else{
      this.toggleSocial = true;
    }
    eventData.stopPropagation();
  }

  ngOnDestroy() {
    // this.auctionSubscription.unsubscribe();
    this.auctionSocket.disconnect();
    clearInterval(this.timer);
  }


  tryParseInt(number){
    return parseInt(Math.floor(number).toString());
  }

  handleBid(eventData,auctionId){
    console.log('try bid for : ',auctionId);
    this.loading.show();

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

  RegisterAuctionSlideupClick(eventData) {
    if(this.toggleSocial){
      this.shared.emitCloseSocial(this.auction.auctionId);
    }
    else{
      if(this.auction.participated){
        this.cart.state = "participated";
      }else if(this.cart.participated){
        this.cart.state = "confirmed";
      }
      else if(this.cart.state=="" || this.cart.state=="closed"){
          this.cart.state = "participate";
      }
    }
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

}
