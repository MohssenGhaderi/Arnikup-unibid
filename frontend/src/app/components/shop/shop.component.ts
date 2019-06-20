import { Component, OnInit, ViewChild, ElementRef, Input } from '@angular/core';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { Shop } from 'src/app/models/shop/shop.model';
import { Buy } from 'src/app/models/shop/buy.model';
import { Links } from 'src/app/links.component';

@Component({
  selector: 'app-shop',
  templateUrl: './shop.component.html',
  styleUrls: ['./shop.component.css']
})
export class ShopComponent implements OnInit {
  items : Shop;
  buy = new Buy();
  loading = true;
  dialog = false;
  Link = Links;

  @Input() shop: Shop;
  @ViewChild('shopWrapper') shopWrapperElem: ElementRef;


  constructor(private mainService: MainServices,public shared:SharingService) { }

  ngOnInit() {
    this.mainService.GetShop().subscribe(result => {
      this.items = result;
      this.loading = false;
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
    const shopWrapper = this.shopWrapperElem.nativeElement as HTMLElement;
    shopWrapper.style.filter = 'blur(3px)';
    this.dialog = true;
  }

  close(){
    const shopWrapper = this.shopWrapperElem.nativeElement as HTMLElement;
    shopWrapper.style.filter = 'none';
    this.dialog = false;
  }

  buyCoin(coinId){
    alert(coinId);
  }

  buyAvatar(avatarId){
    alert(avatarId);
  }
}
