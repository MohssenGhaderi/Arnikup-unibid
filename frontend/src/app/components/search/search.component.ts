import { Component, OnInit, Input, ViewChild, Renderer2, ElementRef} from '@angular/core';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { GetAuctions } from 'src/app/models/service/getAuctions.model';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { ErrorComponent } from 'src/app/components/error/error.component';
import { SuccessComponent } from 'src/app/components/success/success.component';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  searchObj;
  auctions: GetAuctions;
  subscription: any;
  productCount = 0;
  @ViewChild(LoadingComponent) loading: LoadingComponent ;
  @ViewChild(ErrorComponent) error: ErrorComponent ;
  @ViewChild(SuccessComponent) success: SuccessComponent ;
  @ViewChild('mainWrapper') mainWrapperElem: ElementRef;

  constructor(public shared:SharingService,private service:MainServices,private renderer: Renderer2) {
    this.subscription = this.shared.getSearchChangedEmitter().subscribe(result=>{
      this.searchObj = result;
      this.search();
    });
  }

  ngOnInit() {
    const wrapperElem: HTMLElement = document.getElementById('mainWrapper');
    this.renderer.setStyle(wrapperElem, 'justify-content', 'initial');
    this.renderer.setStyle(wrapperElem, 'align-items', 'initial');

    if(this.shared.search.currentId!=-1){
      this.searchObj = {"text":this.shared.search.keyword,"categoryId":this.shared.search.currentId};
    }else{
      this.searchObj = {"text":this.shared.search.keyword};
    }
    this.search();

  }

  search(){
    this.loading.show();
    this.service.SearchAuctions(this.searchObj).subscribe(result=>{
      this.auctions = result;
      this.productCount = this.auctions.lastAuctions.length;
      this.loading.hide();
    });
  }

  ngOnDestroy(){
    this.subscription.unsubscribe();
  }

}
