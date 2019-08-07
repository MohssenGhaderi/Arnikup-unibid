import { Component, OnInit, ViewChild, ElementRef, Input } from '@angular/core';
import { MainServices } from 'src/app/services/main.service';
import { UserService } from 'src/app/services/user.service';
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

  isLoggedIn = false;
  Link = Links;
  userInfo:BasicUserInformation;
  userSyncTimer;
  joined;
  username;

  constructor(
    private userService: UserService,
    private service: MainServices,
    private shared: SharingService,
    private liveUser:LiveUserService) {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      this.isLoggedIn = true;
    }

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
    }, 10000);
  }

  ngDoCheck(){
    // this.auction.started = new StartedAuction();
    if(!this.joined){
      this.joined = true;
      this.liveUser.join();
    }
  }

  shop(){
    this.shared.shop = true;
  }

  nofiy(){
    this.shared.toggleMenu.notification = !this.shared.toggleMenu.notification;
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

  toggleProfileMenu(){
    this.liveUser.getStatus();
    this.shared.toggleMenu.notification = false;
    this.shared.toggleMenu.profile = !this.shared.toggleMenu.profile;
    this.shared.toggleMenu.profileReset();
    this.shared.lastClass = "myCfnAnimation-fadeIn";
  }

  hideProfileMenu(eventData){
    if(eventData){
      if(eventData.target.classList[0]!="profileSelector" && !this.shared.visibleProfile){
        this.userService.hideProfile();
      }
    }
  }

}
