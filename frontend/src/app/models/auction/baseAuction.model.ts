import { Charity } from './charity.model';
import { BaseParticipant } from './baseParticipant.model';
import { Product } from './product.model';
import { AuctionStatus } from './auctionStatus.model';
import { ExtraBids } from './extrabids.model';


export class BaseAuction {
  charity: Charity;
  auctionId: number;
  images : string[];
  level: number;
  maxLevel: number;
  likeCount: number;
  participants: BaseParticipant[];
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
  extraBids:ExtraBids;
}
