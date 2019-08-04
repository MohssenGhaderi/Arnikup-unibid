import { Component, OnInit, ViewChild, Input } from '@angular/core';
import { SharingService } from 'src/app/services/sharing.service';
import { MainServices } from 'src/app/services/main.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component'
import { ErrorComponent } from 'src/app/components/error/error.component'
import { SuccessComponent } from 'src/app/components/success/success.component'
import { ProductDetails } from 'src/app/models/details/details.model'

@Component({
  selector: 'app-product-details',
  templateUrl: './product-details.component.html',
  styleUrls: ['./product-details.component.css']
})
export class ProductDetailsComponent implements OnInit {

  @ViewChild(ErrorComponent ) error: ErrorComponent ;
  @ViewChild(SuccessComponent ) success: SuccessComponent ;
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;
  @Input() auctionId:number;
  productDetails:ProductDetails;

  constructor(private shared:SharingService,private service:MainServices) { }

  ngOnInit() {
    this.loading.show();
    this.service.GetProductDetails(this.auctionId).subscribe(result=>{
      this.loading.hide();
      this.productDetails = result;
      console.log(this.productDetails);
      },
      error=>{
        this.loading.hide();
      })
  }
  close(){
    this.shared.productDetails=false;
  }
}
