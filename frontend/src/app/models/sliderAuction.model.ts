import { Participants } from './participants.model';

export class SliderAuction {
  image: string;
  likeCount: number;
  participants: Participants;
  id: number;
  maxMembers: number;
  liked: boolean;
  participated: boolean;
  tag: string;
  title: string;
  basePrice: number;
  maxPrice: number;
  remainedTime: number;
  day: number;
  hour: number;
  minute: number;
  seconds: number;
}