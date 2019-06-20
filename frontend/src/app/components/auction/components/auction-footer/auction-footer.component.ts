import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { BaseAuction } from 'src/app/models/auction/baseAuction.model';
import { UserService } from 'src/app/services/user.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';

@Component({
  selector: 'app-auction-footer',
  templateUrl: './auction-footer.component.html',
  styleUrls: ['./auction-footer.component.css']
})
export class AuctionFooterComponent implements OnInit {
  @Input() auction: BaseAuction;
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;
  constructor(private userService:UserService) { }

  ngOnInit() {
  }

  addToBasket(eventData,auctionId){
    eventData.preventDefault();
    this.loading.show();
    this.userService.AddOrder({"auctionId":auctionId}).subscribe(result => {
      console.log(result);
      this.loading.hide();
      this.success.show(result,2000);
    },
    error => {
      this.loading.hide();
      this.error.show(error,2000,null);
    });
  }


}
