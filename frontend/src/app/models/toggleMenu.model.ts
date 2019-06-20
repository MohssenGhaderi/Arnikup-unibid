export class ToggleMenu {
  constructor() {
    this.profile = false;
    this.avatar = false;
    this.edit = false;
    this.finance = false;
    this.shoppingCart = false;
    this.information = false;
    this.search = false;
    this.score = false;
    this.preview = false;
    this.address = false;
    this.payment = false;
  }
  public reset (){
    this.profile = false;
    this.avatar = false;
    this.edit = false;
    this.finance = false;
    this.shoppingCart = false;
    this.information = false;
    this.search = false;
    this.score = false;
    this.preview = false;
    this.address = false;
    this.payment = false;
  }
  public profileReset (){
    this.avatar = false;
    this.edit = false;
    this.finance = false;
    this.shoppingCart = false;
    this.information = false;
    this.search = false;
    this.score = false;
    this.preview = false;
    this.address = false;
    this.payment = false;


  }
  profile: boolean;
  avatar: boolean;
  edit : boolean;
  finance: boolean;
  shoppingCart: boolean;
  information: boolean;
  search: boolean;
  score: boolean;
  preview : boolean;
  address : boolean;
  payment : boolean;
}
