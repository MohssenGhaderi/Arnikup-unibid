import { Component, OnInit, Input } from '@angular/core';
import { Message } from 'src/app/models/message.model';

@Component({
  selector: 'app-message-archive-item',
  templateUrl: './message-archive-item.component.html',
  styleUrls: ['./message-archive-item.component.css']
})
export class MessageArchiveItemComponent implements OnInit {

  constructor() { }
  @Input() message:Message;
  toggleAnswer = false;
  toggleMore = false;

  ngOnInit() {
    console.log(this.message.message.length);
  }

  showAnswer(eventData){
    this.toggleAnswer = true;
    eventData.stopPropagation();
  }

  hideAnswer(eventData){
    this.toggleAnswer = false;
    eventData.stopPropagation();
  }

  showMore(eventData){
    this.toggleMore = true;
    eventData.stopPropagation();
  }

  hideMore(eventData){
    this.toggleMore = false;
    eventData.stopPropagation();
  }

}
