export class Search {
  constructor(){
    this.currentIndex = -1;
    this.currentText = "";
    this.keyword = "";
    this.currentId = 0;
    this.visible = false;
    this.operate = false;
    this.max = 0;
    this.min = 0;
  }
  reset(){
    this.currentIndex = -1;
    this.currentText = "";
    this.keyword = "";
    this.currentId = 0;
    this.visible = false;
    this.max = 0;
    this.min = 0;
  }
  inc(){
    if(this.currentIndex < this.max -1 ){
      this.currentIndex ++;
    }
  }
  dec(){
    if(this.currentIndex > this.min){
      this.currentIndex --
    }
  }
  setText(text){
    this.currentText = text;
  }
  currentIndex: number;
  currentId: number;
  max: number;
  min: number;
  currentText : string;
  keyword : string;
  visible: boolean;
  operate: boolean;
}
