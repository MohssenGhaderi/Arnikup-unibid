import { Component, OnInit, Input, ViewChild, ElementRef, HostListener } from '@angular/core';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SharingService } from 'src/app/services/sharing.service'
import { LiveUserService } from 'src/app/services/live-user.service';
import { UserService } from 'src/app/services/user.service';
import { Score } from 'src/app/models/user/information/score.model'
import { Links } from 'src/app/links.component';

@Component({
  selector: 'app-score',
  templateUrl: './score.component.html',
  styleUrls: ['./score.component.css']
})
export class ScoreComponent implements OnInit {

  scores : Score[];
  Link = Links;
  @Input() username: string;
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
    this.el.nativeElement.getElementsByClassName('ScoresContainer')[0].classList.add('myCfnAnimation-slidedown');

    this.liveUser.scores.subscribe(result => {
      this.scores = result;
    });
    this.loading.show();
    this.userService.GetScores().subscribe(result=>{
      this.scores = result;
      this.loading.hide();
    });
  }

  goBack(){
    this.shared.lastClass = "myCfnAnimation-slideup";
    this.el.nativeElement.getElementsByClassName('ScoresContainer')[0].classList.add('myCfnAnimation-slidedown-none');
    setTimeout(()=>{
      this.shared.toggleMenu.profile = true;
      this.shared.toggleMenu.score = false;
    },200);
  }
}
