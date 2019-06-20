import { Component, OnInit, Renderer2 } from '@angular/core';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveAuctionService } from 'src/app/services/live-auction.service';

@Component({
  selector: 'app-default',
  templateUrl: './default.component.html',
  styleUrls: ['./default.component.css']
})
export class DefaultComponent implements OnInit {

  constructor(private renderer: Renderer2,public shared:SharingService,private auctionSocket:LiveAuctionService) {
  }

  ngOnInit() {
    const wrapperElem: HTMLElement = document.getElementById('mainWrapper');
    this.renderer.setStyle(wrapperElem, 'justify-content', 'initial');
    this.renderer.setStyle(wrapperElem, 'align-items', 'initial');
  }
}
