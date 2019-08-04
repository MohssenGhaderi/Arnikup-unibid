import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { AuctionStatus } from '../models/auction/auctionStatus.model';
import { Winner } from '../models/auction/winner.model';
import { States } from '../models/auction/states.model';
import { LiveUser } from '../models/liveUser.model';
import { GetError } from '../models/service/getError.model';
import { SuccessMessage } from '../models/success.message.model';
import { GetAuction } from 'src/app/models/service/getAuction.model';
import { AuctionItem } from 'src/app/models/auction/auctionItem.model';


@Injectable({
  providedIn: 'root'
})
export class LiveAuctionService {
  connect = this.socket.fromEvent<string>('connect');
  status = this.socket.fromEvent<AuctionStatus>('status');
  winner = this.socket.fromEvent<Winner>('winner');
  joined = this.socket.fromEvent<string>('joined');
  leaved = this.socket.fromEvent<string>('leaved');
  failed = this.socket.fromEvent<GetError>('failed');
  succeed = this.socket.fromEvent<SuccessMessage>('succeed');
  accepted = this.socket.fromEvent<string>('accepted');
  bids = this.socket.fromEvent<string>('remainBids');
  users = this.socket.fromEvent<LiveUser[]>('users');
  auction = this.socket.fromEvent<GetAuction>('auction');
  auctionItem = this.socket.fromEvent<AuctionItem>('auctionItem');
  remained = this.socket.fromEvent<string>('remained');
  done = this.socket.fromEvent<string>('done');
  states = this.socket.fromEvent<States>('states');

  constructor(private socket: Socket) {
    console.log('socket constructor');
  }

  connectToServer(){
    this.socket.connect();
  }

  leave(auctionId){
    this.socket.emit('leave',{'auctionId':auctionId});
  }

  join(auctionId){
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      this.socket.emit('join',{'auctionId':auctionId,'authorization':token});
    }
  }

  getStatus(auctionId){
    this.socket.emit('getStatus',{'auctionId':auctionId});
  }

  getStates(auctionId){
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      this.socket.emit('getStates',{'auctionId':auctionId,'authorization':token});
    }
  }

  getAuction(auctionId){
    this.socket.emit('getAuction',{'auctionId':auctionId});
  }

  offerBid(auctionId){
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      this.socket.emit('bid',{'auctionId':auctionId,'authorization':token});
    }
  }
  getUsers(auctionId){
    this.socket.emit('getUsers',{'auctionId':auctionId});
  }

  disconnect(){
    this.socket.disconnect();
  }

}
