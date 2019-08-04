import { Charity } from './charity.model';
import { Participants } from './participants.model';
import { Coin } from './coin.model';
import { AuctionPlan } from './auctionPlan.model';
import { AuctionStatus } from './auctionStatus.model';


export class Auction {
  charity: Charity;
  participants: Participants;
  coins: Coin[];
  auctionId: number;
  level: number;
  maxLevel: number;
  maxMembers: number;
  image: string;
  liked: boolean;
  likeCount: number;
  participated: boolean;
  plan: AuctionPlan;
  status: AuctionStatus;
  bids : number;
  tag: string;
  title: string;
  basePrice: number;
  maxPrice: number;
  discount: number;
  remainedTime: number;
}
