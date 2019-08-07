import { Component, OnInit, Input, ViewChild, ElementRef, HostListener } from '@angular/core';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { UserService } from 'src/app/services/user.service';
import { GetTransactions } from 'src/app/models/service/getTransactions.model';
import { Links } from 'src/app/links.component';

@Component({
  selector: 'app-transaction',
  templateUrl: './transaction.component.html',
  styleUrls: ['./transaction.component.css']
})
export class TransactionComponent implements OnInit {

    trans : GetTransactions;
    Link = Links;
    @Input() coins: number;
    @Input() gems: number;
    currentTransactions;
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
      this.el.nativeElement.getElementsByClassName('ScoresContainer')[0].classList.add('myCfnAnimation-slidedown');

      // this.liveUser.scores.subscribe(result => {
      //   this.scores = result;
      // });

      this.loading.show();

      this.userService.GetTransactions(this.moreObj).subscribe(result=>{
        this.trans = result;
        this.loading.hide();
      });

    }

    showMore(eventData){
      if(this.trans.transactions.length < this.trans.total){
        this.moreObj["start"] = this.trans.transactions.length;
        this.moreObj["stop"] = this.moreObj["start"] + 5;
        this.loading.show();
        this.userService.GetTransactions(this.moreObj).subscribe(result=>{
          result.transactions.forEach(item=>{
            this.trans.transactions.push(item);
          })
          this.loading.hide();
        });
      }
      eventData.stopPropagation();
    }

    applyGems(eventData){
      if(!this.timer){
        this.loading.show();
        this.userService.ApplyGem().subscribe(result=>{
          result.transactions.forEach(item=>{
            this.trans.transactions.splice(0, 0, item);
          });
          this.loading.hide();
          this.gems -= 1;
          var aggregatedCoins = this.coins + result.addedGems;

          this.timer = setInterval(() => {
            if(this.coins < aggregatedCoins){
              this.coins += 1;
            }else{
              clearInterval(this.timer);
              this.timer = null;
            }
          }, 10);

        },error => {
          this.error.show(error,2000,'/signin');
        });
      }
      eventData.stopPropagation();
    }

    goBack(){
      this.shared.lastClass = "myCfnAnimation-slideup";
      this.el.nativeElement.getElementsByClassName('ScoresContainer')[0].classList.add('myCfnAnimation-slidedown-none');
      setTimeout(()=>{
        this.shared.toggleMenu.profile = true;
        this.shared.toggleMenu.transaction = false;
      },200);
    }
  }
