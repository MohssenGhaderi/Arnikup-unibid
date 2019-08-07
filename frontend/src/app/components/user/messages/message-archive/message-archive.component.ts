import { Component, OnInit, Input, ViewChild, ElementRef, HostListener } from '@angular/core';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { UserService } from 'src/app/services/user.service';
import { GetMessages } from 'src/app/models/service/getMessages.model';

@Component({
  selector: 'app-message-archive',
  templateUrl: './message-archive.component.html',
  styleUrls: ['./message-archive.component.css']
})
export class MessageArchiveComponent implements OnInit {

  msg : GetMessages;
  timer;
  moreObj = {"start":0,"stop":5};
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  constructor(private el: ElementRef, private shared:SharingService,private liveUser:LiveUserService,private userService:UserService) { }
  @HostListener('mouseenter') onMouseEnter() {
    this.shared.visibleProfile = true;
  }
  @HostListener('mouseleave') onMouseLeave() {
    this.shared.visibleProfile = false;
  }
  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('ScoresContainer')[0].classList.add('myCfnAnimation-slideright');

    this.loading.show();

    this.userService.GetMessages(this.moreObj).subscribe(result=>{
      this.msg = result;
      this.loading.hide();
    });

  }

  showMore(eventData){
    if(this.msg.messages.length < this.msg.total){
      this.moreObj["start"] = this.msg.messages.length;
      this.moreObj["stop"] = this.moreObj["start"] + 5;
      this.loading.show();
      this.userService.GetMessages(this.moreObj).subscribe(result=>{
        result.messages.forEach(item=>{
          this.msg.messages.push(item);
        })
        this.loading.hide();
      });
    }
    eventData.stopPropagation();
  }

  goBack(){
    this.shared.lastClass = "myCfnAnimation-slideleft";
    this.el.nativeElement.getElementsByClassName('ScoresContainer')[0].classList.add('myCfnAnimation-slideright-none');
    setTimeout(()=>{
      this.shared.toggleMenu.messages = true;
      this.shared.toggleMenu.messageArchive = false;
    },200);
  }
}
