import { Component, OnInit ,Input ,ViewChild ,ElementRef,ViewChildren } from '@angular/core';
import { BaseAuction } from 'src/app/models/auction/baseAuction.model';
import { LiveAuctionService } from 'src/app/services/live-auction.service';
import { ProgressComponent } from 'src/app/components/progress/progress.component';
import { Router } from '@angular/router';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { Links } from 'src/app/links.component';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { SharingService } from 'src/app/services/sharing.service';
import { States } from 'src/app/models/auction/states.model';

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
  @ViewChild(ProgressComponent) progress: ProgressComponent ;
  subscription1: any;
  subscription2: any;
  isLoggedIn = false;
  remainedTime;
  timer;
  timeoutId;
  auctionTimer;
  joined = false;
  Link = Links;
  done = false;
  autobid = false;
  states = new States();
  checked = false;
  statusbar = false;
  process = true;
  serverRespond = false;
  totalTest = 13;
  currentTest = 13;

  constructor(
    private auctionSocket:LiveAuctionService,
    private router:Router,
    private authService:AuthenticationService,
    private shared:SharingService
  )
  {
    this.auctionSocket.connectToServer();
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      this.isLoggedIn = true;
    }

    this.subscription1 = this.shared.getExtraBidsChangedEmitter().subscribe(result=>{
        this.auction.bids = result.bids;
        this.startLoading().then(()=>{
          if(this.success){
            this.success.show(result,2000).then(()=>{
              this.stopLoading();
            });
          }
        });
    });

    this.subscription2 = this.shared.getExtraBidsErrorEmitter().subscribe(result=>{
        this.startLoading().then(()=>{
          if(this.error){
            this.error.show({"error":{"message":result}},2000).then(()=>{
              this.stopLoading();
            });
          }
        });
    });
  }

  loadingPreprocess(){
    return new Promise((resolve)=>{
        this.process = true;
        setTimeout(()=>{
          resolve(this.process);
        },100);
      })
  }

  startLoading(){
    return new Promise((resolve)=>{
        this.loadingPreprocess().then(()=>{
          if(this.loading){
            this.loading.show()
          }
          resolve(true);
        });
      })
  }

  stopLoading(){
    return new Promise((resolve)=>{
        if(this.loading){
          this.loading.hide();
          this.process = false;
        }
        resolve(this.process);
      })
  }

  ngOnInit() {

    this.auctionSocket.connect.subscribe(result =>
      {
        console.log(result);
        this.serverRespond = true;
        setInterval(()=>{
          if(this.serverRespond){
            this.auctionSocket.keepaliveServer();
            this.serverRespond = false;
          }
        },3000);

      });

      this.auctionSocket.keepalive.subscribe(result => {
         console.log(result);
         this.serverRespond = true;
       });

    this.auctionSocket.iceAge.subscribe(result => {
      console.log(result);
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.states.iceAge = true;
        this.states.holliDay = false;
        this.states.hotSpot = false;
        this.states.feniTto = false;
        this.states.noWinner = false;
        this.auction.remainedTime = result.heartbeat;
        this.auctionSocket.getAuction(this.auction.auctionId);
        this.StartTimer();
      }
    });

    this.auctionSocket.holliDay.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.states.iceAge = false;
        this.states.holliDay = true;
        this.states.hotSpot = false;
        this.states.feniTto = false;
        this.states.noWinner = false;
        if(!this.joined){
          this.joined = true;
          this.startLoading();
          this.auctionSocket.PublicRoom(this.auction.auctionId);
          this.auctionSocket.PrivateRoom(this.auction.auctionId);
        }
      }
    });

    this.auctionSocket.hotSpot.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.states.iceAge = false;
        this.states.holliDay = true;
        this.states.hotSpot = false;
        this.states.feniTto = false;
        this.states.noWinner = false;
        if(!this.joined){
          this.joined = true;
          this.startLoading();
          this.auctionSocket.PublicRoom(this.auction.auctionId);
          this.auctionSocket.PrivateRoom(this.auction.auctionId);
        }
        if(this.timer){
          this.StopTimer();
        }
        this.auction.remainedTime = result.heartbeat;

        if(this.shared.autobid.state && !this.autobid){
          if ((this.auction.remainedTime <= (this.shared.autobid.deadline * 1000 + 800)) && !this.auction.done){
            this.auctionSocket.offerBid(this.auction.auctionId);
            this.autobid = true;
          }
        }

      }
    });

    this.auctionSocket.joined.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.auctionSocket.getStatus(this.auction.auctionId);
        this.stopLoading();
      }
    });

    this.auctionSocket.status.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.auction.status = result.status;
        this.stopLoading();
      }
    });

    this.auctionSocket.bids.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.auction.bids = result.bids;
        if(this.auction.extraBids && !this.shared.extraBidUsed && this.auction.bids <= this.auction.extraBids.target){
          this.shared.extraBid = true;
        }
      }
    this.stopLoading();
    });

    this.auctionSocket.reset.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.auction.remainedTime = result.heartbeat;
        this.progress.reset(this.tryParseInt(this.auction.remainedTime/1000),10);
        this.autobid = false;
        this.stopLoading();
      }
    });

    this.auctionSocket.zeroTime.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.StopTimer();
        this.startLoading().then(()=>{
          if(this.success){
            this.success.show(result,2000);
          }
        });
      }
    });

    this.auctionSocket.feniTto.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.startLoading().then(()=>{
          if(this.error){
            this.error.show(result,2000).then(()=>{
              this.stopLoading();
              this.states.iceAge = false;
              this.states.holliDay = false;
              this.states.hotSpot = false;
              this.states.feniTto = false;
              this.states.noWinner = true;
            })
          }
        });
      }
    });

    this.auctionSocket.winner.subscribe(result => {
      if(this.auction && this.auction.auctionId===result.auctionId){
        this.auction.status = result.winner;
        this.states.iceAge = false;
        this.states.holliDay = false;
        this.states.hotSpot = false;
        this.states.feniTto = true;
        this.states.noWinner = false;
        this.auction.done = true;
        this.stopLoading();
      }
    });

    this.auctionSocket.failed.subscribe(result => {
      this.startLoading().then(()=>{
        if(this.error){
          this.error.show(result,1000,null).then(()=>{
            this.stopLoading();
          });
        }
      });
    });
  }

  ngAfterViewInit(){

    // this.startLoading().then(()=>{
    //   this.loading.show();
    //   this.success.show({"message":"success is working"},2000).then(()=>{
    //     this.error.show({"error":{"message":"error is working"}},3000).then(()=>{
    //       this.loading.hide();
    //
    //       this.loading.show();
    //       this.success.show({"message":"another success is working"},2000).then(()=>{
    //         this.error.show({"error":{"message":"another error is working"}},3000).then(()=>{
    //           this.loading.hide();
    //           this.stopLoading();
    //         });
    //       })
    //     });
    //   });
    // });

  }
  StartTimer(){

    if(!this.timer){
      this.remainedTime = this.ConvertMS(this.auction.remainedTime);
      this.timer = setInterval(() => {
        this.auction.remainedTime -= 1000;
        this.remainedTime = this.ConvertMS(this.auction.remainedTime);
      }, 1000);
    }

  }

  StopTimer(){
    if(this.timer){
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  ngDoCheck(){

      if(this.auction && !this.checked){
        this.checked = true;
        this.StartTimer();
        if(this.auction.remainedTime < -3000 && this.auction.status.name==="بدون پیشنهاد"){
          this.states.iceAge = false;
          this.states.holliDay = false;
          this.states.hotSpot = false;
          this.states.feniTto = false;
          this.states.noWinner = true;
        }
      }
  }

  handleBid(eventData,auctionId){
    this.startLoading();
    this.auctionSocket.offerBid(auctionId);
    eventData.stopPropagation();
  }

  ngOnDestroy(){
    this.auctionSocket.disconnect();
    this.subscription1.unsubscribe();
    this.subscription2.unsubscribe();
    //clearInterval(this.timer);
  }

  tryParseInt(number){
    return parseInt(Math.floor(number).toString());
  }

  reset(){
    this.totalTest = 10;
    this.currentTest = 10;
    this.progress.reset(this.currentTest,this.totalTest);
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
