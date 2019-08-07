import { Component, OnInit, ViewChild, ElementRef, Renderer2 } from '@angular/core';
import { UserService } from 'src/app/services/user.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { FavAuction } from 'src/app/models/auction/favorite.model';

@Component({
  selector: 'app-favorite',
  templateUrl: './favorite.component.html',
  styleUrls: ['./favorite.component.css']
})
export class FavoriteComponent implements OnInit {
  items = [0,1,2,3,4,5];
  @ViewChild('mainWrapper') mainWrapperElem: ElementRef;
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;
  auctions: FavAuction[];
  subscription: any;
  constructor(public shared:SharingService,private service:UserService,private renderer: Renderer2){ }

  ngOnInit() {

    this.subscription = this.shared.getDeleteLikeEmitter().subscribe(result=>{
      this.auctions = this.auctions.filter(obj => {
          return obj.auctionId != result;
      });
    });

    const wrapperElem: HTMLElement = document.getElementById('mainWrapper');
    this.renderer.setStyle(wrapperElem, 'justify-content', 'initial');
    this.renderer.setStyle(wrapperElem, 'align-items', 'initial');
    this.shared.toggleMenu.reset();

    this.loading.show();
    this.service.GetFavAuctions().subscribe(result => {
      this.auctions = result;
      this.loading.hide();
      this.items = [];
    },
    error => {
      this.loading.hide();
      this.items = [];
    });

  }

  hideProfileMenu(eventData){
    if(!this.shared.visibleProfile){
        this.service.hideProfile();
    }
  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
  }

}
