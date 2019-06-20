import { Component, OnInit, ViewChild, QueryList, ElementRef, ViewChildren } from '@angular/core';
import { UserService } from 'src/app/services/user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { Payment } from 'src/app/models/user/information/payment.model'
import { Links } from 'src/app/links.component';

@Component({
  selector: 'app-finance',
  templateUrl: './finance.component.html',
  styleUrls: ['./finance.component.css']
})
export class FinanceComponent implements OnInit {
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;
  Link = Links;
  payments:Payment[];

  constructor(private el: ElementRef, private userService:UserService,private shared:SharingService,private liveUser:LiveUserService) { }

  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('financeContainer')[0].classList.add('myCfnAnimation-slideright');

    this.loading.show();
    this.userService.GetPaymentInformation().subscribe(result=>{
      this.payments = result;
      this.loading.hide();
    },
    error=>{
      this.loading.hide();
      this.error.show(error,2000,'/signin');
    });
  }

  goBack(){
    this.shared.lastClass = "myCfnAnimation-slideleft";
    this.el.nativeElement.getElementsByClassName('financeContainer')[0].classList.add('myCfnAnimation-slideright-none');
    setTimeout(()=>{
      this.shared.toggleMenu.finance = false;
      this.shared.toggleMenu.profile = true;
    },200);

  }
}
