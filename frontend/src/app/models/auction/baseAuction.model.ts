import { Charity } from './../charity.model';
import { Participant } from './participant.model';
import { Product } from './product.model';
import { AuctionStatus } from './../auctionStatus.model';


export class BaseAuction {
  charity: Charity;
  auctionId: number;
  images : string[];
  level: number;
  maxLevel: number;
  likeCount: number;
  participants: Participant[];
  maxMembers: number;
  liked: boolean;
  participated: boolean;
  bids : number;
  tag: string;
  title: string;
  basePrice: number;
  maxPrice: number;
  remainedTime: number;
  discount: number;
  product:Product;
  started:boolean;
  status:AuctionStatus;
  done:boolean;
}
