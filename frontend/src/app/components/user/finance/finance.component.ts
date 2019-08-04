import { Component, OnInit, ViewChild, QueryList, ElementRef, ViewChildren, HostListener } from '@angular/core';
import { UserService } from 'src/app/services/user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LiveUserService } from 'src/app/services/live-user.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { Links } from 'src/app/links.component';
import { PaymentInfo } from 'src/app/models/user/information/paymentInfo.model'


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
  payments:PaymentInfo[];
  now = Date.now();
  totalDiscount = 0;

  constructor(private el: ElementRef, private userService:UserService,private shared:SharingService,private liveUser:LiveUserService) { }
  @HostListener('mouseenter') onMouseEnter() {
    this.shared.visibleProfile = true;
  }
  @HostListener('mouseleave') onMouseLeave() {
    this.shared.visibleProfile = false;
  }
  ngOnInit() {

    this.el.nativeElement.getElementsByClassName('financeContainer')[0].classList.add('myCfnAnimation-slideright');

    this.loading.show();
    this.userService.GetPaymentInformation().subscribe(result=>{
      this.payments = result;
      this.payments.forEach((item)=> {
       this.totalDiscount += parseInt(item.discount.toString());
     });
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

  readMore(eventData){
    const state = eventData.target.dataset.collapse;
    console.log(state);
    if (state === "true") {
          eventData.target.dataset.collapse = "false";
          eventData.target.previousElementSibling.classList.add('accountProfile-financialCredit-item-info-wide');
          eventData.target.querySelector('a').textContent = 'کمتر';
          eventData.target.querySelector('img').src = 'assets/resources/images/assets/png/toppurle.png';
        }
        else {
          eventData.target.dataset.collapse = "true";
          eventData.target.previousElementSibling.classList.remove('accountProfile-financialCredit-item-info-wide');
          eventData.target.querySelector('a').textContent = 'بیشتر';
          eventData.target.querySelector('img').src = 'assets/resources/images/assets/png/001-down-arrow-copy-6.png';
        }
  }
}
