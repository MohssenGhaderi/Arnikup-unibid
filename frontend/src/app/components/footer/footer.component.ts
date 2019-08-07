import { Component, OnInit, HostListener, ElementRef } from '@angular/core';
import { ScrollEvent } from 'ngx-scroll-event';
import { SharingService } from 'src/app/services/sharing.service';


@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css']
})
export class FooterComponent implements OnInit {

  constructor(private shared:SharingService) { }

  ngOnInit() {

  }

  public handleScroll(event: ScrollEvent) {
    //console.log('scroll occurred', event.originalEvent);
    if (event.isReachingBottom) {
      if (!this.shared.busyScroll){
        console.log(`the user is reaching the bottom`);
        this.shared.busyScroll = true;
        this.shared.emitScrollReached('end');
      }
    }
    // if (event.isReachingTop) {
    //   console.log(`the user is reaching the top`);
    // }
    // if (event.isWindowEvent) {
    //   console.log(`This event is fired on Window not on an element.`);
    // }

  }

}
