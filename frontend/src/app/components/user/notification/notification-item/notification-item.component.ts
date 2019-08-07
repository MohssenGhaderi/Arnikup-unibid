import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { Notification } from 'src/app/models/user/notification.model';
import { UserService } from 'src/app/services/user.service';
import { Router } from '@angular/router';
import { SharingService } from 'src/app/services/sharing.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { Links } from 'src/app/links.component';

@Component({
  selector: 'app-notification-item',
  templateUrl: './notification-item.component.html',
  styleUrls: ['./notification-item.component.css']
})
export class NotificationItemComponent implements OnInit {
  @Input() notification:Notification;
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  Link = Links;
  

  constructor(private service:UserService,private router:Router,private shared:SharingService) { }

  ngOnInit() {
  }

  markAsRead(eventData){
    this.loading.show();
    this.service.MarkAsReadNotification({"notificationId":this.notification.notificationId,"notificationType":this.notification.notificationType}).subscribe(result=>{
      this.loading.hide();
      this.notification.seen = true;
      // this.router.navigate([this.notification.link]);
    },error=>{
      this.error.show(error);
    });
    eventData.stopPropagation();
  }

  DeleteNotification(eventData){
    this.loading.show();
    this.service.DeleteNotification({"notificationId":this.notification.notificationId,"notificationType":this.notification.notificationType}).subscribe(result=>{
      this.loading.hide();
      this.shared.emitDeleteNotification(this.notification);
    },error=>{
      this.error.show(error);
    });
    eventData.stopPropagation();
  }

}
