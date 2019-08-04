import { Component, OnInit, Renderer2, ElementRef, ViewChild } from '@angular/core';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveAuctionService } from 'src/app/services/live-auction.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-default',
  templateUrl: './default.component.html',
  styleUrls: ['./default.component.css']
})
export class DefaultComponent implements OnInit {

  @ViewChild('mainWrapper') mainWrapperElem: ElementRef;

  constructor(
    private renderer: Renderer2,
    public shared:SharingService,
    private auctionSocket:LiveAuctionService,
    private userService: UserService)
    {}

  ngOnInit() {
    const wrapperElem: HTMLElement = document.getElementById('mainWrapper');
    this.renderer.setStyle(wrapperElem, 'justify-content', 'initial');
    this.renderer.setStyle(wrapperElem, 'align-items', 'initial');
  }

  hideProfileMenu(eventData){
    if(!this.shared.visibleProfile){
        this.userService.hideProfile();
    }
  }
}
