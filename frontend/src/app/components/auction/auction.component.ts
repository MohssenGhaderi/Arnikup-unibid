import { Component, OnInit, ElementRef,ViewChild,Renderer2 } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MainServices } from 'src/app/services/main.service';
import { GetAuction } from 'src/app/models/service/getAuction.model';
import { Router } from '@angular/router';
import { LiveAuctionService } from 'src/app/services/live-auction.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';

@Component({
  selector: 'app-auction',
  templateUrl: './auction.component.html',
  styleUrls: ['./auction.component.css']
})
export class AuctionComponent implements OnInit {
  auction: GetAuction;
  timeoutId;
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;

  constructor(
    private route: ActivatedRoute,
    private mainService: MainServices,
    private router:Router,
    private auctionSocket:LiveAuctionService,
    private renderer: Renderer2,
    private shared:SharingService,
  )
  {this.auctionSocket.connectToServer();}

  ngOnInit() {

    this.renderer.setStyle(document.getElementsByClassName('wrapper')[0], 'background-color', "#fff");
    this.route.params.subscribe(params => {
      this.loading.show();
        this.mainService.GetAuction(params['id']).subscribe(result => {
          this.auction = result;
          this.loading.hide();
        },
        error => {
          this.loading.hide();
          this.error.show(error,2000,'/');
        });
    });

    this.auctionSocket.auction.subscribe(result=>{
      this.auction = result;
    });

    this.auctionSocket.remained.subscribe(result=>{
      console.log(result);
    });
  }
}
