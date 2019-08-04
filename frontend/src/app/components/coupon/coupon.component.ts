import { Component, OnInit, ViewChild, ElementRef, Input  } from '@angular/core';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';
import { UserService } from 'src/app/services/user.service';


@Component({
  selector: 'app-coupon',
  templateUrl: './coupon.component.html',
  styleUrls: ['./coupon.component.css']
})
export class CouponComponent implements OnInit {

  couponCode;
  @ViewChild('couponButton') couponButton: ElementRef ;
  @ViewChild('couponInput') couponInput: ElementRef ;

  @Input() title: string;
  @Input() operation: string;

  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;


  constructor(private el:ElementRef,private service:UserService) { }

  ngOnInit() {
    if(this.operation==="check"){
      this.couponInput.nativeElement.classList.add('off-content-text');
    }
  }

  onCouponChange(value){
    this.couponCode = value;
    if(this.couponCode===''){
      this.couponButton.nativeElement.classList.remove('accountProfile-basket-onButton');
      this.couponButton.nativeElement.classList.add('accountProfile-basket-offButton');
    }else{
      this.couponButton.nativeElement.classList.remove('accountProfile-basket-offButton');
      this.couponButton.nativeElement.classList.add('accountProfile-basket-onButton');
    }
  }

  confirm(){
    this.loading.show();
    if(this.operation==="check"){
      this.service.CheckCoupon({"couponCode":this.couponCode}).subscribe(result=>{
        this.loading.hide();
        this.success.show(result,6000);
      },
      error=>{
        this.loading.hide();
        this.error.show(error,3000,null);
      });
    }else{
      this.service.ApplyCoupon({"couponCode":this.couponCode}).subscribe(result=>{
        this.loading.hide();
        this.success.show(result,6000);
      },
      error=>{
        this.loading.hide();
        this.error.show(error,2000,null);
      });
    }
  }

}
