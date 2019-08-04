import { Component, OnInit, ViewChild, QueryList, ElementRef, ViewChildren ,HostListener} from '@angular/core';
import { UserService } from 'src/app/services/user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { Avatar } from 'src/app/models/user/avatar.model'
import { Links } from 'src/app/links.component';


@Component({
  selector: 'app-avatar',
  templateUrl: './avatar.component.html',
  styleUrls: ['./avatar.component.css']
})
export class AvatarComponent implements OnInit {
  avatars : Avatar[];
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;
  @ViewChildren('avatarItems') avatarItems:QueryList<ElementRef>;

  Link = Links;
  makeChanges = false;
  selected = new Avatar();
  userSyncTimer;
  firstTime;

  constructor(private el: ElementRef, private userService:UserService,private shared:SharingService,private liveUser:LiveUserService) { }
  @HostListener('mouseenter') onMouseEnter() {
    this.shared.visibleProfile = true;
  }
  @HostListener('mouseleave') onMouseLeave() {
    this.shared.visibleProfile = false;
  }
  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('AvatarContainer')[0].classList.add('myCfnAnimation-slideright');
    this.loading.show();

    this.userService.GetAvatars().subscribe(result => {
      this.avatars = result;
      this.loading.hide();
    },
    error => {
      this.error.show(error,2000,'/signin');
    });

  }
  ngAfterViewInit(){
    this.liveUser.avatars.subscribe(result=>{
      this.avatars = result;
    });
  }

  ngAfterViewChecked(){
    if(this.avatarItems && !this.makeChanges){
      var myArray = ['brownBackground', 'semiYellowBackground', 'orangeBackground', 'greenBackground'];
      for(var i = 0 ; i < this.avatarItems.length; i++)
      {
        this.makeChanges = true;
        var rand = myArray[Math.floor(Math.random() * myArray.length)];
        this.avatarItems.toArray()[i].nativeElement.classList.add(rand);

      }
    }
  }

  selectAvatar(event,Id){
    this.firstTime = true;
    for(var i = 0 ; i < this.avatarItems.length; i++)
    {
      if(this.avatars[i].avatarId!=Id){
        this.avatarItems.toArray()[i].nativeElement.classList.remove('selectAvatar-item-active');
      }else{
        this.selected = this.avatars[i];
        this.avatarItems.toArray()[i].nativeElement.classList.add('selectAvatar-item-active');
      }
    }
  }

  goBack(){
    this.shared.lastClass = "myCfnAnimation-slideleft";
    this.el.nativeElement.getElementsByClassName('AvatarContainer')[0].classList.add('myCfnAnimation-slideright-none');
    setTimeout(()=>{
      this.shared.toggleMenu.profile = true;
      this.shared.toggleMenu.avatar = false;
    },200);

  }

  confirmAvatar(eventData){
    this.liveUser.getProfileStatus();
    this.liveUser.getStatus();
    eventData.preventDefault();
    this.loading.show();
    this.userService.SaveAvatar({"avatarId":this.selected.avatarId}).subscribe(result=>{
      this.success.show(result,1500)
      .then(()=>{
        this.loading.hide();
        this.goBack();
      });
    },
    error => {
      this.loading.hide();
      this.error.show(error,3000);
    });
  }

}
