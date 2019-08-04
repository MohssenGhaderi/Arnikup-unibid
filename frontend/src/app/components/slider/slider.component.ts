import { Component, OnInit } from '@angular/core';
import Swiper from 'swiper';
import { GetSliderAuctions } from 'src/app/models/service/sliderAuctions.model';
import { MainServices } from 'src/app/services/main.service';
import { Links } from 'src/app/links.component'

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.css']
})
export class SliderComponent implements OnInit {
  sliderAuctions: GetSliderAuctions;
  loading = true;
  Link = Links;
  mySwiper : Swiper;

  constructor(private mainService: MainServices) { }

  ngOnInit() {

  }

  ngAfterViewInit() {

    this.mainService.GetSliderAuctions().subscribe(result => {
      this.sliderAuctions = result;
      this.loading = false;
      setTimeout(function () {
        this.mySwiper = new Swiper('.swiper-container', {
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



    //var mySwiper = document.querySelector('.swiper-container').nativeElement.swiper;
    //this.mySwiper.init();
  }


  // config: SwiperOptions = {
  //   autoplay: 3000, // Autoplay option having value in milliseconds
  //   initialSlide: 1, // Slide Index Starting from 0
  //   // slidesPerView: 1, // Slides Visible in Single View Default is 1
  //   nextButton: '.swiper-button-next', // Class for next button
  //   prevButton: '.swiper-button-prev', // Class for prev button
  //   spaceBetween: 30, // Space between each Item,
  //   slidesPerView: 'auto',
  //   centeredSlides: true,
  //
  // };

  // config: SwiperOptions = {
  //   navigation: {
  //         nextEl: '.swiper-button-next',
  //         prevEl: '.swiper-button-prev',
  //         spaceBetween: 30
  //       },
  // };

}
