import { AuctionStatus } from './auctionStatus.model';


export class FinishedAuction {
  auctionId: number;
  image : string;
  level: number;
  maxLevel: number;
  maxMembers: number;
  liked: boolean;
  participated: boolean;
  title: string;
  basePrice: number;
  maxPrice: number;
  date: string;
  discount: number;
  status:AuctionStatus;
  done:boolean;
}
