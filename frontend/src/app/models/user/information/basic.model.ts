import { Notification } from './../notification.model'

export class BasicUserInformation {
  coins:number;
  gems:number;
  notifications:Notification[];
  username:string;
  avatar:string;
  level:number;
}
