import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-loading',
  templateUrl: './loading.component.html',
  styleUrls: ['./loading.component.css']
})
export class LoadingComponent implements OnInit {
  showMe = false;
  constructor() { }

  ngOnInit() {
  }

  show(){
    this.showMe = true;
  }

  hide(){
    this.showMe = false;
  }

}
