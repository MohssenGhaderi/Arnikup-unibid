import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Auction } from '../models/auction/auction.model';
import { GetAuctions } from '../models/service/getAuctions.model';
import { GetAuction } from '../models/service/getAuction.model';
import { Shop } from '../models/shop/shop.model';
import { GetSliderAuctions } from '../models/service/sliderAuctions.model';
import { GetFinishedAuctions } from '../models/service/getFinishedAuctions.model';

import { SearchItems } from '../models/service/searchItems.model';
import { Links } from '../links.component';
import { BasicUserInformation } from '../models/user/information/basic.model'
import { ProductDetails } from '../models/details/details.model'
import { GetParticipation } from '../models/auction/getParticipation.model'


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
  HandleExtraBidUrl = Links.prefix+'/v2/api/auction/extrabids';
  searchUrl = Links.prefix+'v2/api/search';
  finishedUrl = Links.prefix+'v2/api/site/finished/auctions';
  productDetailsUrl = Links.prefix+'v2/api/auction/details/';

  constructor(private http: HttpClient) { }

  FinishedAuctions() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<GetFinishedAuctions>(this.finishedUrl , httpOptions);
    } else {
      return this.http.get<GetFinishedAuctions>(this.finishedUrl);
    }

  }

  SearchAuctions(searchObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<GetAuctions>(
        this.searchUrl,
        { params: searchObj,
          headers: new HttpHeaders(
            {
              Authorization: 'Bearer ' + token
            }
          )});
    } else {
      return this.http.get<GetAuctions>(this.searchUrl, {params: searchObj} );
    }
  }

  GetProductDetails(auctionId) {
    return this.http.get<ProductDetails>(this.productDetailsUrl+auctionId);
  }

  HandleExtraBid(auctionObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.post(this.HandleExtraBidUrl, auctionObj , httpOptions);
    } else {
      return this.http.post(this.HandleExtraBidUrl, auctionObj);
    }

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
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<GetSliderAuctions>(this.sliderAuctionUrl , httpOptions);
    }else{
      return this.http.get<GetSliderAuctions>(this.sliderAuctionUrl);
    }
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
      return this.http.post<GetParticipation>(this.participationByCoin ,participationObject,httpOptions);
    }else{
      return this.http.post<GetParticipation>(this.participationByCoin ,participationObject);
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
      return this.http.post<GetParticipation>(this.participationByGem ,participationObject,httpOptions);
    }else{
      return this.http.post<GetParticipation>(this.participationByGem ,participationObject);
    }
  }
}
