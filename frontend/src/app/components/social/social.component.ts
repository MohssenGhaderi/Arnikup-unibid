import { Component, OnInit, Input, ElementRef, HostListener } from '@angular/core';
import { SharingService } from 'src/app/services/sharing.service';

@Component({
  selector: 'app-social',
  templateUrl: './social.component.html',
  styleUrls: ['./social.component.css']
})
export class SocialComponent implements OnInit {
  @Input() title:string;
  @Input() auctionId:string;
  @Input() description:string;
  @Input() url:string;
  subscription: any;
  visibleMe = false;

  constructor(private el:ElementRef,public shared:SharingService) { }
  @HostListener('mouseenter') onMouseEnter() {
    this.visibleMe = true;
  }
  @HostListener('mouseleave') onMouseLeave() {
    this.visibleMe = false;
  }
  ngOnInit() {
    this.el.nativeElement.getElementsByClassName('social-container')[0].classList.add('myCfnAnimation-slideup');
    this.subscription = this.shared.getSocialCloserEmitter().subscribe((auctionId)=>{
      if(this.auctionId==auctionId && !this.visibleMe){
        this.el.nativeElement.getElementsByClassName('social-container')[0].classList.add('myCfnAnimation-slideup-none');
        this.shared.emitSocialStay(this.auctionId);
      }
    });
  }
  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

}
