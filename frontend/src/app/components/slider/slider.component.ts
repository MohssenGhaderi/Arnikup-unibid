import { Component, OnInit } from '@angular/core';
import Swiper from 'swiper';
import { GetSliderAuctions } from 'src/app/models/service/sliderAuctions.model';
import { MainServices } from 'src/app/services/main.service';
import { Links } from 'src/app/links.component'
import { SharingService } from 'src/app/services/sharing.service';


@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.css']
})
export class SliderComponent implements OnInit {
  sliderAuctions: GetSliderAuctions;
  Link = Links;
  private static mySwiper : Swiper;
  subscription: any;

  constructor(private mainService: MainServices,private shared:SharingService) { }

  ngOnInit() {

  }

  ngAfterViewInit() {

    this.subscription = this.shared.getScrollReachedEmitter().subscribe(result=>{
      var searchObj = {"start":this.shared.auctions,"stop":this.shared.auctions+3};

      this.mainService.GetSliderAuctionsLazy(searchObj).subscribe(result => {

        result.sliderAuctions.forEach(item=>{
          this.sliderAuctions.sliderAuctions.push(item);
        });

        SliderComponent.mySwiper.destroy(true,true);
        setTimeout(function () {
          SliderComponent.mySwiper = new Swiper('.swiper-container', {
            centeredSlides: true,
            spaceBetween: 30,
            initialSlide: 1,
            slidesPerView: 'auto',
            navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
          });
        },100);
      },
      error => {
      });
    });

    this.mainService.GetSliderAuctions().subscribe(result => {
      this.sliderAuctions = result;

      setTimeout(function () {
        SliderComponent.mySwiper = new Swiper('.swiper-container', {
          centeredSlides: true,
          spaceBetween: 30,
          initialSlide: 1,
          slidesPerView: 'auto',
          navigation: {
                  nextEl: '.swiper-button-next',
                  prevEl: '.swiper-button-prev',
              },
        });
      },100);
    },
    error => {
    });

  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
    this.shared.busyScroll = false;
  }




}
