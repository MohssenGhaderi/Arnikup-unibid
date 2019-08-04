import { Component, OnInit, Input , ElementRef, ViewChild} from '@angular/core';
import { PaymentServices } from 'src/app/services/payment.service';
import { UserService } from 'src/app/services/user.service';
import { Buy } from 'src/app/models/shop/buy.model';
import { SharingService } from 'src/app/services/sharing.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';

@Component({
  selector: 'app-confirm',
  templateUrl: './confirm.component.html',
  styleUrls: ['./confirm.component.css']
})
export class ConfirmComponent implements OnInit {

  @Input() buy: Buy;
  @Input() shopWrapperElem: ElementRef;
  loaded;
  redirectToBankLink;

  @ViewChild(ErrorComponent ) error: ErrorComponent ;
  @ViewChild(SuccessComponent ) success: SuccessComponent ;
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;

  constructor(public shared:SharingService,private service: PaymentServices,private userService:UserService,) { }

  ngOnInit() {
    const shopWrapper = this.shopWrapperElem.nativeElement as HTMLElement;
    shopWrapper.style.filter = 'blur(3px)';

  }

  ngDoCheck(){
    if(!this.loaded && this.loading){
      this.loaded = true;
      if(this.loading){
        switch(this.buy.type){
          case 'coin':{
            this.loading.show();
            this.service.BuyCoin({"coinId":this.buy.Id}).subscribe(result=>{
              this.success.show(result,1000).then(()=>{
                this.service.PaymentGateway({"GUID":result.GUID}).subscribe(pay=>{
                  console.log(pay);
                  console.log('redirect to bank');
                },
                error=>{
                  this.loading.hide();
                  this.error.show(error,3000,null);
                });
              });
            },
            error =>{
              this.loading.hide();
              this.error.show(error,3000,null);
            });

            break;
          };
          case 'gem':{
            this.loading.show();
            this.service.BuyGem({"gemId":this.buy.Id}).subscribe(result=>{
              this.success.show(result,1000).then(()=>{
                this.service.PaymentGateway({"GUID":result.GUID}).subscribe(pay=>{
                  console.log(pay);
                  console.log('redirect to bank');
                },
                error=>{
                  this.loading.hide();
                  this.error.show(error,3000,null);
                });
              });
            },
            error =>{
              this.loading.hide();
              this.error.show(error,3000,null);
            });

            break;
          };
          case 'chest':{
            this.loading.show();
            this.service.BuyChest({"chestId":this.buy.Id}).subscribe(result=>{
              this.success.show(result,1000).then(()=>{
                this.service.PaymentGateway({"GUID":result.GUID}).subscribe(pay=>{
                  console.log(pay);
                  console.log('redirect to bank');
                },
                error=>{
                  this.loading.hide();
                  this.error.show(error,3000,null);
                });
              });
            },
            error =>{
              this.loading.hide();
              this.error.show(error,3000,null);
            });

            break;
          };
          case 'avatar':{

            break;
          };
          case 'product':{
            console.log('buy product');
            break;
          };
        }
      }
    }
  }

  confirm(eventData){
    eventData.preventDefault();
    switch(this.buy.type){
      case 'coin':{
        break;
      };
      case 'gem':{

        break;
      };
      case 'chest':{

        break;
      };
      case 'avatar':{
        this.loading.show();
        this.userService.SaveAvatar({"avatarId":this.buy.Id}).subscribe(result=>{
          this.success.show(result,2000).then(()=>{
            this.close();
          });
        },
        error =>{
          this.loading.hide();
          this.error.show(error,2000,null).then(()=>{
            this.close();
          });
        });

        break;
      };
      case 'product':{
        console.log('buy product');
        break;
      };
    }
  }

  close(){
    const shopWrapper = this.shopWrapperElem.nativeElement as HTMLElement;
    shopWrapper.style.filter = 'none';
    this.shared.showConfirm = false;
  }

}
