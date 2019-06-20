import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Auction } from '../models/auction.model';
import { GetAuctions } from '../models/service/getAuctions.model';
import { GetAuction } from '../models/service/getAuction.model';
import { Shop } from '../models/shop/shop.model';
import { GetSliderAuctions } from '../models/service/sliderAuctions.model';
import { SearchItems } from '../models/service/searchItems.model';
import { Links } from '../links.component';
import { BasicUserInformation } from '../models/user/information/basic.model'


@Injectable({ providedIn: 'root' })
export class MainServices {
  getAuctionsUrl = Links.prefix+'/v2/api/site/last/auctions';
  getShopUrl = Links.prefix+'/v2/api/shop';
  sliderAuctionUrl = Links.prefix+'/v2/api/site/slider/auctions';
  searchItemsUrl =  Links.prefix+'/v2/api/site/categories';
  likeUrl = Links.prefix+'/v2/api/auction/like';
  getAuctionUrl = Links.prefix+'/v2/api/auction/';
  participationByCoin = Links.prefix+'/v2/api/auction/coin/registeration';
  participationByGem = Links.prefix+'/v2/api/auction/gem/registeration';
  getBasicInfoUrl = Links.prefix+'/v2/api/user/basic';

  constructor(private http: HttpClient) {

  }

  GetBasicInformation() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<BasicUserInformation>(this.getBasicInfoUrl , httpOptions);
    } else {
      return this.http.get<BasicUserInformation>(this.getBasicInfoUrl);
    }

  }

  GetAuctions() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<GetAuctions>(this.getAuctionsUrl , httpOptions);
    } else {
      return this.http.get<GetAuctions>(this.getAuctionsUrl);
    }

  }

  GetShop() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<Shop>(this.getShopUrl , httpOptions);
    } else {
      return this.http.get<Shop>(this.getShopUrl);
    }

  }

  GetSliderAuctions() {
    const headers = new HttpHeaders();
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      headers.set('Authorization', token);
    }
    return this.http.get<GetSliderAuctions>(this.sliderAuctionUrl , {headers});
  }

  GetSearchItems() {
    return this.http.get<SearchItems>(this.searchItemsUrl);
  }

  likeAuction(auction) {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          'Authorization':`Bearer ${token}`
        })
      };
      return this.http.post(this.likeUrl ,auction,httpOptions);
    }else{
      return this.http.post(this.likeUrl ,auction);
    }
  }

  GetAuction(auctionId) {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          'Authorization':`Bearer ${token}`
        })
      };
      return this.http.get<GetAuction>(this.getAuctionUrl+auctionId,httpOptions);
    }else{
      return this.http.get<GetAuction>(this.getAuctionUrl+auctionId);
    }
  }

  registerByCoin(participationObject) {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          'Authorization':`Bearer ${token}`
        })
      };
      return this.http.post(this.participationByCoin ,participationObject,httpOptions);
    }else{
      return this.http.post(this.participationByCoin ,participationObject);
    }
  }

  registerByGem(participationObject) {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          'Authorization':`Bearer ${token}`
        })
      };
      return this.http.post(this.participationByGem ,participationObject,httpOptions);
    }else{
      return this.http.post(this.participationByGem ,participationObject);
    }
  }
}
