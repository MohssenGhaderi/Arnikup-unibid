import { Component, OnInit, Input, ElementRef } from '@angular/core';
import Swiper from 'swiper';
import { BaseAuction } from 'src/app/models/auction/baseAuction.model';
import { Links } from 'src/app/links.component';
import { LiveAuctionService } from 'src/app/services/live-auction.service';


@Component({
  selector: 'app-auction-slider',
  templateUrl: './auction-slider.component.html',
  styleUrls: ['./auction-slider.component.css']
})
export class AuctionSliderComponent implements OnInit {
  @Input() auction: BaseAuction;
  Link = Links;
  status;
  mySwiper : Swiper;

  constructor(private el:ElementRef, private auctionSocket:LiveAuctionService) {
    this.auctionSocket.connectToServer();
  }

  ngOnInit() {
    this.auctionSocket.status.subscribe(result =>{
      this.status = result;
    });
  }
  ngAfterViewInit(){
    setTimeout(function () {
      this.mySwiper = new Swiper('.swiper-container', {
        centeredSlides: true,
        spaceBetween: 30,
        initialSlide: 0,
        slidesPerView: 'auto',
        navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
      });
    },500);
  }
}
