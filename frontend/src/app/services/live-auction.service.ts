import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { States } from '../models/auction/states.model';
import { ErrorMessage } from '../models/socket/error.model';
import { SuccessMessage } from '../models/success.message.model';
import { GetAuction } from 'src/app/models/service/getAuction.model';
import { AuctionLive } from 'src/app/models/socket/auction.model';
import { Joined } from 'src/app/models/socket/joined.model';
import { Leaved } from 'src/app/models/socket/leaved.model';
import { Status } from 'src/app/models/socket/status.model';
import { HeartBeat } from 'src/app/models/socket/heartbeat.model';
import { Bids } from 'src/app/models/socket/bids.model';
import { EndState } from 'src/app/models/socket/endState.model';
import { AuctionWinner } from '../models/socket/winner.model';
import { AuctionUsers } from '../models/socket/users.model';


@Injectable({
  providedIn: 'root'
})
export class LiveAuctionService {
  connect = this.socket.fromEvent<string>('connect');
  status = this.socket.fromEvent<Status>('status');
  joined = this.socket.fromEvent<Joined>('joined');
  leaved = this.socket.fromEvent<Leaved>('leaved');
  failed = this.socket.fromEvent<ErrorMessage>('failed');
  succeed = this.socket.fromEvent<SuccessMessage>('succeed');
  accepted = this.socket.fromEvent<string>('accepted');
  keepalive = this.socket.fromEvent<string>('keepalive');
  bids = this.socket.fromEvent<Bids>('bids');
  users = this.socket.fromEvent<AuctionUsers>('users');
  auction = this.socket.fromEvent<GetAuction>('auction');
  auctionItem = this.socket.fromEvent<AuctionLive>('auctionItem');

  reset = this.socket.fromEvent<HeartBeat>('reset');
  iceAge = this.socket.fromEvent<HeartBeat>('iceAge');
  holliDay = this.socket.fromEvent<HeartBeat>('holliDay');
  hotSpot = this.socket.fromEvent<HeartBeat>('hotSpot');
  stayAlive = this.socket.fromEvent<HeartBeat>('stayAlive');
  zeroTime = this.socket.fromEvent<EndState>('zeroTime');
  feniTto = this.socket.fromEvent<EndState>('feniTto');
  winner = this.socket.fromEvent<AuctionWinner>('winner');

  constructor(private socket: Socket) {
    console.log('socket constructor');
  }

  connectToServer(){
    this.socket.connect();
  }
  
  keepaliveServer(){
    this.socket.emit("keepalive");
  }

  leave(auctionId){
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      this.socket.emit('leave',{'auctionId':auctionId,'authorization':token});
    }
  }

  PrivateRoom(auctionId){
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      this.socket.emit('join_private',{'auctionId':auctionId,'authorization':token});
    }
  }

  PublicRoom(auctionId){
    this.socket.emit('join_public',{'auctionId':auctionId});
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
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      this.socket.emit('getAuction',{'auctionId':auctionId,'authorization':token});
    }
  }

  getAuctionItem(auctionId){
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      this.socket.emit('getAuctionItem',{'auctionId':auctionId,'authorization':token});
    }
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
