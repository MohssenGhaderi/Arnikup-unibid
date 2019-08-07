import { Component, OnInit, Input } from '@angular/core';
import { UserCoupon } from 'src/app/models/user/userCoupon.model';

@Component({
  selector: 'app-coupon-item',
  templateUrl: './coupon-item.component.html',
  styleUrls: ['./coupon-item.component.css']
})
export class CouponItemComponent implements OnInit {
  @Input() userCoupon:UserCoupon;

  constructor() { }

  ngOnInit() {
  }

}
