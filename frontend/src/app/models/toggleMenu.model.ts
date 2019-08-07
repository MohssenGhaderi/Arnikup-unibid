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
    this.password = false;
    this.notification = false;
    this.transaction = false;
    this.messages = false;
    this.messageArchive = false;
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
    this.password = false;
    this.notification = false;
    this.transaction = false;
    this.messages = false;
    this.messageArchive = false;
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
    this.password = false;
    this.transaction = false;
    this.messages = false;
    this.messageArchive = false;
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
  password : boolean;
  notification : boolean;
  transaction :boolean;
  messages :boolean;
  messageArchive :boolean;
}
