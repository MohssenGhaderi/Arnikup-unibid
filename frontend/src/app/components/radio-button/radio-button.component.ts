import { Component, OnInit, Input, ViewChildren, ElementRef, QueryList } from '@angular/core';
import { SharingService } from 'src/app/services/sharing.service';

@Component({
  selector: 'app-radio-button',
  templateUrl: './radio-button.component.html',
  styleUrls: ['./radio-button.component.css']
})
export class RadioButtonComponent implements OnInit {

  items = [{"id":1,"title":"موبایل"},{"id":2,"title":"ایمیل"}];
  selectedItem = {"id":1,"title":"موبایل"};

  numbers;
  @ViewChildren('chkElements') checkElements:QueryList<ElementRef>;

  constructor(private el:ElementRef,private shared:SharingService) { }

  ngOnInit() {

  }

  check(eventData){

    this.checkElements.forEach(chkItem => {
      chkItem.nativeElement.classList.replace('radio-check-circle-fill','radio-check-circle');
    });

    eventData.target.classList.add('radio-check-circle-fill');
    this.shared.emitChangeGuestMessageType(eventData.target.nextSibling.textContent);

    eventData.stopPropagation();
  }

}
