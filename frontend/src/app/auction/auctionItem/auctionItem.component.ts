import { Component, OnInit, Input, ViewChild, ElementRef ,ViewChildren, QueryList} from '@angular/core';
import { MainServices } from 'src/app/_services/main.service';
import { AuthenticationService } from 'src/app/_services/authentication.service';
import { Auction } from 'src/app/models/auction.model';
import { Links } from 'src/app/links.component';
import { Router } from '@angular/router';
import { GetParticipation } from 'src/app/models/getParticipation.model';
import { ProgressComponent } from 'src/app/progress/progress.component';


@Component({
  selector: 'app-auctionItem',
  templateUrl: './auctionItem.component.html',
  styleUrls: ['./auctionItem.component.css']
})

export class AuctionItemComponent implements OnInit {
  toggleHeart = false;
  showRegisterAuction = false;
  hideRegisterAuction = false;
  loading = false;
  errorObj = null;
  coinState = 'pallet';
  GetParticipation = GetParticipation;
  participated = false;
  Link = Links;
  remainedTime;
  timeoutId = 0;

  @Input() auction: Auction;
  @ViewChild('errorMessage') errorMessageElem: ElementRef;
  @ViewChild(ProgressComponent) progress;

  currentTime = Math.floor(Math.random() * (10 - 4)) + 4;
  totalSegments = 10 ;

  constructor(
    private service: MainServices,
    private authService:AuthenticationService,
    private router: Router
  )
  {
  }

  ngOnInit() {


    console.log('auction component');
    this.toggleHeart = this.auction.liked;

    if (this.auction) {
      this.remainedTime = this.ConvertMS(this.auction.remainedTime);
      setInterval(() => {
        this.auction.remainedTime = this.auction.remainedTime - 1000;
        this.remainedTime = this.ConvertMS(this.auction.remainedTime);

      }, 1000);
    }

  }
  ngAfterViewInit() {

  }

  tryParseInt(number){
    return parseInt(Math.floor(number));
  }

  resetProgress(eventData){
    console.log('reset');
    // this.progresses.reset();
    // eventData.stopPropagation();
  }

  toggleClick(eventData, auctionId) {

      this.loading = true;
      this.service.likeAuction({auctionId:auctionId}).subscribe(result => {
        this.toggleHeart = !this.toggleHeart;
        this.loading = false;
      },
      error => {

        this.errorObj = error;
        this.loading = false;
        this.errorMessageElem.nativeElement.classList.add('cfnAnimation-fadeIn');
        clearTimeout(this.timeoutId);
        this.timeoutId = setTimeout(() => {
          if(error.status==401){
            this.authService.logout();
            this.router.navigate(['/signin']);
          }
          this.errorMessageElem.nativeElement.classList.remove('cfnAnimation-fadeIn');
        }, 2000);
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
    this.loading = true;
    this.service.registerByCoin({auctionId:auctionId,planId:planId}).subscribe(result => {
      this.loading = false;
      this.GetParticipation = <any>result;
      this.coinState = 'confirmed';
      this.participated = true;
    },
    error => {
      if(error.error.reason==="coins"){
        this.GetParticipation = error.error;
        this.coinState = 'gems';
      }

      this.errorObj = error;
      this.loading = false;
      this.errorMessageElem.nativeElement.classList.add('cfnAnimation-fadeIn');
      clearTimeout(this.timeoutId);
      this.timeoutId = setTimeout(() => {
        this.errorMessageElem.nativeElement.classList.remove('cfnAnimation-fadeIn');
        if(error.status==401){
          this.authService.logout();
          this.router.navigate(['/signin']);
        }
      }, 2000);
    });
    eventData.stopPropagation();
  }

  registerByGem(eventData,auctionId,planId){
    eventData.stopPropagation();

    this.loading = true;
    this.service.registerByGem({auctionId:auctionId,planId:planId}).subscribe(result => {
      this.loading = false;
      this.GetParticipation = <any>result;
      this.coinState = 'confirmed';
      this.participated = true;
    },
    error => {
      if(error.error.reason==="coins"){
        this.GetParticipation = error.error;
        this.coinState = 'gems';
      }

      this.errorObj = error;
      this.loading = false;
      this.errorMessageElem.nativeElement.classList.add('cfnAnimation-fadeIn');
      clearTimeout(this.timeoutId);
      this.timeoutId = setTimeout(() => {
        this.errorMessageElem.nativeElement.classList.remove('cfnAnimation-fadeIn');
        if(error.status===401){
          this.authService.logout();
          this.router.navigate(['/signin']);
        }
      }, 2000);
    });

  }
}
