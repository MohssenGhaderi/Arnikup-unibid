import { Component, OnInit,ViewChildren, ElementRef, QueryList, Input,Renderer2 ,Injectable} from '@angular/core';

@Component({
  selector: 'app-progress',
  templateUrl: './progress.component.html',
  styleUrls: ['./progress.component.css']
})

@Injectable({ providedIn: 'root' })
export class ProgressComponent implements OnInit {

  @Input() current: number;
  @Input() total: number;

  @ViewChildren('progresses') progresses:QueryList<ElementRef>;

  timer;
  time;
  numbers;

  constructor(private el: ElementRef) {

  }

  ngOnInit() {
    this.numbers = Array.apply(null, {length: this.total}).map(Number.call, Number);
  }

  reset(current,total) {
    this.stop();
    this.current = current;
    this.total = total;
    this.numbers = []
    this.numbers = Array.apply(null, {length: total}).map(Number.call, Number);

    this.progresses.forEach(progressItem => {
      progressItem.nativeElement.classList.replace('progressItemNone','progressItem');
      progressItem.nativeElement.classList.remove('progressItem-empty');
    });

    for(var i = this.progresses.length -1 ; i >= this.current; i--)
    {
      this.progresses.toArray()[i].nativeElement.classList.replace('progressItem','progressItemNone');
    }

    this.time = this.current;
    this.start();
  }

  init(){

    if(this.progresses.length > 0){
      for(var i = this.progresses.length -1 ; i >= this.current; i--)
      {
        this.progresses.toArray()[i].nativeElement.classList.replace('progressItem','progressItemNone');
      }
      this.time = this.current;
    }
  }

  ngAfterViewInit(){
    this.init();
    this.start();
  }
  start(){
    clearInterval(this.timer);
    this.timer =  setInterval(()=> {
      this.time -= 1;
      if(this.time <= -1){
        console.log('progress done');
        this.stop();
      }
      else{
        if(this.time>=10){
          this.el.nativeElement.getElementsByClassName('progressItem')[this.el.nativeElement.getElementsByClassName('progressItem').length-1].remove();
        }else{
          var current_element = this.el.nativeElement.getElementsByClassName('progressItem-empty')[0];
          if(current_element && current_element.previousElementSibling){
            current_element.previousElementSibling.classList.add('progressItem-empty');
          }else{
            current_element = this.el.nativeElement.getElementsByClassName('progressItem')[this.el.nativeElement.getElementsByClassName('progressItem').length-1];
            if(current_element){
              current_element.classList.add('progressItem-empty');
            }else{
              this.progresses.toArray()[this.progresses.length-1].nativeElement.classList.add('progressItem-empty');
            }
          }
        }
      }
    }, 1000);
  }

  stop(){
    clearInterval(this.timer);
  }

  ngOnDestroy() {
    clearInterval(this.timer);
  }

}
