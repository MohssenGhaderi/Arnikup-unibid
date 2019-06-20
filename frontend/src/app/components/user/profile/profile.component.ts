import { Component, OnInit, ViewChild, ElementRef} from '@angular/core';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { UserService } from 'src/app/services/user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { Links } from 'src/app/links.component';
import { MainUserInformation } from 'src/app/models/user/information/main.model'

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  userMainInfo:MainUserInformation;
  Link = Links;
  userSyncTimer;

  constructor(private el: ElementRef,private userService:UserService,private shared:SharingService,private liveUser:LiveUserService) {
  }
  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('accountProfile-profile-header')[0].classList.add(this.shared.lastClass);

    this.userSyncTimer = setInterval(() => {
      this.liveUser.getProfileStatus();
    }, 1000);

    this.loading.show();

    this.userService.GetMainInformation().subscribe(result => {
      this.userMainInfo = result;
      this.loading.hide();
    },
    error => {
      this.error.show(error,2000,'/signin');
    });
  }

  ngAfterViewInit(){
    this.liveUser.profileStatus.subscribe(result=>{
      this.userMainInfo = result;
    });
  }

  toggleAvatar(){
    this.shared.toggleMenu.reset();
    this.shared.toggleMenu.avatar = true;
  }

  toggleFinance(){
    this.shared.toggleMenu.reset();
    this.shared.toggleMenu.finance = true;
  }

  toggleShoppingCard(){
    this.shared.toggleMenu.reset();
    this.shared.basketClass = "myCfnAnimation-slideup";
    this.shared.toggleMenu.shoppingCart = true;
  }

  toggleScore(){
    this.shared.toggleMenu.reset();
    this.shared.toggleMenu.score = true;
  }

  toggleEditProfile(){
    this.shared.toggleMenu.reset();
    this.shared.toggleMenu.edit = true;
  }


}
