import { Component, OnInit, Input, ViewChild, ElementRef, HostListener } from '@angular/core';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SharingService } from 'src/app/services/sharing.service'
import { LiveUserService } from 'src/app/services/live-user.service';
import { UserService } from 'src/app/services/user.service';
import { GetNotifications } from 'src/app/models/service/getNotifications.model';
import { Links } from 'src/app/links.component';

@Component({
  selector: 'app-notification',
  templateUrl: './notification.component.html',
  styleUrls: ['./notification.component.css']
})
export class NotificationComponent implements OnInit {
    subscription: any;
    notifs : GetNotifications;
    Link = Links;
    @Input() username: string;
    @ViewChild(LoadingComponent) loading: LoadingComponent ;
    @ViewChild(ErrorComponent) error: ErrorComponent ;
    moreObj = {"start":0,"stop":5};
    constructor(private el: ElementRef, private shared:SharingService,private liveUser:LiveUserService,private userService:UserService) {

      this.subscription = this.shared.getDeleteNotificationEmitter().subscribe(result=>{
        this.notifs.notifications = this.notifs.notifications.filter(obj => {
            return obj != result;
        });
      });

    }
    @HostListener('mouseenter') onMouseEnter() {
      this.shared.visibleProfile = true;
    }
    @HostListener('mouseleave') onMouseLeave() {
      this.shared.visibleProfile = false;
    }
    ngOnInit() {
      this.el.nativeElement.getElementsByClassName('notification')[0].classList.add('myCfnAnimation-fadeIn');

      this.loading.show();
      this.userService.GetNotifications(this.moreObj).subscribe(result=>{
        console.log(result);
        this.notifs = result;
        this.loading.hide();
      },error=>{
        this.error.show(error);
      });
    }

    showMore(eventData){
      if(this.notifs.notifications.length < this.notifs.total){
        this.moreObj["start"] = this.notifs.notifications.length;
        this.moreObj["stop"] = this.moreObj["start"] + 5;
        this.loading.show();
        this.userService.GetNotifications(this.moreObj).subscribe(result=>{
          result.notifications.forEach(item=>{
            this.notifs.notifications.push(item);
          })
          this.loading.hide();
        },error=>{
          this.error.show(error);
        });
      }
      eventData.stopPropagation();
    }

    goBack(){
      this.shared.lastClass = "myCfnAnimation-slideup";
      this.el.nativeElement.getElementsByClassName('notification')[0].classList.add('myCfnAnimation-fadeOut');
      setTimeout(()=>{
        this.shared.toggleMenu.notification = false;
      },200);
    }

    ngOnDestroy(){
      this.subscription.unsubscribe();
    }
  }
