import { Component, OnInit, Input, ViewChildren, ElementRef, QueryList } from '@angular/core';

@Component({
  selector: 'app-color',
  templateUrl: './color.component.html',
  styleUrls: ['./color.component.css']
})
export class ColorComponent implements OnInit {
  @Input() colors:string[];
  @ViewChildren('colorElements') colorElements:QueryList<ElementRef>;

  constructor() { }

  ngOnInit() {

  }

  ngAfterViewInit(){

      for(var i = 0  ; i < this.colorElements.length; i++)
      {
        console.log(this.colorElements.toArray()[i].nativeElement,this.colors[i]);
        this.colorElements.toArray()[i].nativeElement.classList.add(this.colors[i]);
      }
  }

}
