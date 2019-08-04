import { Participants } from './participants.model';

export class SliderAuction {
  image: string;
  likeCount: number;
  participants: Participants;
  auctionId: number;
  maxMembers: number;
  liked: boolean;
  participated: boolean;
  tag: string;
  title: string;
  basePrice: number;
  maxPrice: number;
  remainedTime: number;
}
