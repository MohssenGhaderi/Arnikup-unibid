import { Component, OnInit } from '@angular/core';
import { GetSliderAuctions } from '../models/service/sliderAuctions.model';
import { MainServices } from '../_services/main.service';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.css']
})
export class SliderComponent implements OnInit {
  toggleHeart = false;
  sliderAuctions: GetSliderAuctions;
  loading = true;
  constructor(private mainService: MainServices) { }

  ngOnInit() {
    this.mainService.GetSliderAuctions().subscribe(result => {
      this.sliderAuctions = result;
      this.loading = false;
    },
    error => {
    });
  }

  config: SwiperOptions = {
    autoplay: 3000, // Autoplay option having value in milliseconds
    initialSlide: 1, // Slide Index Starting from 0
    // slidesPerView: 1, // Slides Visible in Single View Default is 1
    nextButton: '.swiper-button-next', // Class for next button
    prevButton: '.swiper-button-prev', // Class for prev button
    spaceBetween: 30, // Space between each Item,
    slidesPerView: 'auto',
    centeredSlides: true,

  };

  toggleClick(eventData) {
    this.toggleHeart = !this.toggleHeart;
    eventData.stopPropagation();
  }

}
