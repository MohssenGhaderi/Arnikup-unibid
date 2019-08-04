import { Component, OnInit, ViewChild, ElementRef, Renderer2 } from '@angular/core';
import { MainServices } from 'src/app/services/main.service';
import { SharingService } from 'src/app/services/sharing.service';
import { LoadingComponent } from 'src/app/components/loading/loading.component';
import { GetFinishedAuctions } from 'src/app/models/service/getFinishedAuctions.model';


@Component({
  selector: 'app-held',
  templateUrl: './held.component.html',
  styleUrls: ['./held.component.css']
})
export class HeldComponent implements OnInit {
  items = [0,1,2,3,4,5];
  @ViewChild('mainWrapper') mainWrapperElem: ElementRef;
  @ViewChild(LoadingComponent ) loading: LoadingComponent ;
  auctions: GetFinishedAuctions;
  constructor(public shared:SharingService,private service:MainServices,private renderer: Renderer2){ }

  ngOnInit() {
    const wrapperElem: HTMLElement = document.getElementById('mainWrapper');
    this.renderer.setStyle(wrapperElem, 'justify-content', 'initial');
    this.renderer.setStyle(wrapperElem, 'align-items', 'initial');

    this.loading.show();
    this.service.FinishedAuctions().subscribe(result => {
      this.auctions = result;
      this.loading.hide();
      this.items = [];
    },
    error => {
    });

  }



}
