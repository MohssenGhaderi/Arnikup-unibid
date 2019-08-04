import {Details} from './details.model'
export class Cart {
  constructor(){
    this.scroll = false;
    this.auctionId = 0;
    this.state="";
    this.participated = false;
  }
  scroll:boolean;
  auctionId:number;
  state: string;
  participated: boolean;
  details:Details;
}
