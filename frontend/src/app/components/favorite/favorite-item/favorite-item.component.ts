import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { FavAuction } from 'src/app/models/auction/favorite.model';
import { Links } from 'src/app/links.component';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';

@Component({
  selector: 'app-favorite-item',
  templateUrl: './favorite-item.component.html',
  styleUrls: ['./favorite-item.component.css']
})
export class FavoriteItemComponent implements OnInit {
  @Input() auction: FavAuction;
  Link = Links;
  @ViewChild(ErrorComponent ) error: ErrorComponent ;
  @ViewChild(SuccessComponent ) success: SuccessComponent ;
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;
  remainedTime;
  timer;
  constructor(private service: MainServices,private shared:SharingService) { }

  ngOnInit() {
    if(!this.timer){
      this.remainedTime = this.ConvertMS(this.auction.remainedTime);
      this.timer = setInterval(() => {
        if(this.auction.remainedTime > 1000){
          this.auction.remainedTime = this.auction.remainedTime - 1000;
          this.remainedTime = this.ConvertMS(this.auction.remainedTime);
        }else{
          this.shared.DeleteLike.emit(this.auction.auctionId);
        }
      }, 1000);
    }
  }

  toggleClick(eventData, auctionId) {
      this.loading.show();
      this.service.likeAuction({auctionId:auctionId}).subscribe(result => {
        this.loading.hide();
        this.shared.DeleteLike.emit(this.auction.auctionId);
      },
      error => {
        this.loading.hide();
        this.error.show(error,2000,null);
      });
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
