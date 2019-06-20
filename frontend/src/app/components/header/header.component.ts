import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { SearchItems } from 'src/app/models/service/searchItems.model';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { Links } from 'src/app/links.component';
import { BasicUserInformation } from 'src/app/models/user/information/basic.model'

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  @ViewChild('txtSearch') txtSearch: ElementRef;
  @ViewChild('searchToolbarSuggestion') searchToolbarSuggestion: ElementRef;
  searchItems: SearchItems;
  isLoggedIn = false;
  Link = Links;
  toggleProfile = false;
  userInfo:BasicUserInformation;
  userSyncTimer;
  joined;
  username;

  constructor(
    private service: MainServices,
    private shared: SharingService,
    private liveUser:LiveUserService) {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      this.isLoggedIn = true;
    }

    this.service.GetSearchItems().subscribe(result => {
      this.searchItems = result;
    },
    error => {
    });

    this.service.GetBasicInformation().subscribe(result => {
      this.userInfo = result;
      this.username = this.userInfo.username;
    },
    error => {
      localStorage.removeItem('currentUser');
      this.isLoggedIn = false;
    });

   }

  ngOnInit() {
    this.userSyncTimer = setInterval(() => {
      this.liveUser.getStatus();
    }, 1000);
  }

  ngDoCheck(){
    // this.auction.started = new StartedAuction();
    if(!this.joined){
      this.joined = true;
      this.liveUser.join();
    }

  }

  ngAfterViewInit(){
    this.liveUser.connect.subscribe(result => console.log(result));

    this.liveUser.status.subscribe(result => {
      this.userInfo = result;
    });
  }

  ngOnDestroy() {
    this.liveUser.leave();
    this.liveUser.disconnect();
    clearInterval(this.userSyncTimer);
  }

  searchBoxBehaviour(event) {
      this.searchToolbarSuggestion.nativeElement.classList.add('search-toolbar-suggestion-show');
  }

  searchItemClick(eventData) {
    this.txtSearch.nativeElement.value = eventData.target.textContent + ' ';
    this.txtSearch.nativeElement.focus();
    this.searchToolbarSuggestion.nativeElement.classList.remove('search-toolbar-suggestion-show');
  }

  toggleProfileMenu(){
    this.shared.toggleMenu.profile = !this.shared.toggleMenu.profile;
    this.shared.toggleMenu.profileReset();
    this.shared.lastClass = "myCfnAnimation-fadeIn";
  }

  headerClicked(eventData){
    // console.log(eventData.target);
    // console.log('header clicked');
  }


}
