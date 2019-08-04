import { Component, OnInit, ViewChild, ElementRef, Input } from '@angular/core';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { Shop } from 'src/app/models/shop/shop.model';
import { Buy } from 'src/app/models/shop/buy.model';
import { Links } from 'src/app/links.component';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';

@Component({
  selector: 'app-shop',
  templateUrl: './shop.component.html',
  styleUrls: ['./shop.component.css']
})
export class ShopComponent implements OnInit {
  items : Shop;
  buy = new Buy();
  Link = Links;

  @Input() shop: Shop;
  @Input() mainWrapperElem: ElementRef;
  @ViewChild('shopWrapper') shopWrapperElem: ElementRef;
  @ViewChild(ErrorComponent ) error: ErrorComponent ;
  @ViewChild(SuccessComponent ) success: SuccessComponent ;
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;

  constructor(private mainService: MainServices,public shared:SharingService) { }

  ngOnInit() {
    this.loading.show();
    const mainWrapper = this.mainWrapperElem.nativeElement as HTMLElement;
    mainWrapper.style.filter = 'blur(2px)';

    this.mainService.GetShop().subscribe(result => {
      this.items = result;
      this.loading.hide();
    },
    error => {
    });
  }

  buyItem(Id,type,title,pic,price){
    this.buy.Id = Id;
    this.buy.type = type;
    this.buy.title = title;
    this.buy.picture = pic;
    this.buy.price = price;
    this.shared.showConfirm = true;
  }

  close(){
    const mainWrapper = this.mainWrapperElem.nativeElement as HTMLElement;
    mainWrapper.style.filter = 'none';
    this.shared.shop = false;
  }
}
