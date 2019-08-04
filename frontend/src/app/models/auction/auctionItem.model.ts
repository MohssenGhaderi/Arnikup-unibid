import { Charity } from './charity.model';
import { Participants } from './participants.model';
import { Product } from './product.model';
import { AuctionStatus } from './auctionStatus.model';

export class AuctionItem {
  charity: Charity;
  auctionId: number;
  image : string;
  level: number;
  maxLevel: number;
  likeCount: number;
  participants: Participants;
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
