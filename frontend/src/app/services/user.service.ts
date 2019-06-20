import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Shop } from '../models/shop/shop.model';
import { Links } from '../links.component';
import { MainUserInformation } from '../models/user/information/main.model'
import { Cart } from '../models/user/information/cart.model'
import { Score } from '../models/user/information/score.model'
import { Avatar } from '../models/user/avatar.model'
import { EditUserInformation } from 'src/app/models/user/information/edit.model'
import { ShipmentInformation } from 'src/app/models/user/information/shipment.model'
import { Address } from 'src/app/models/user/information/address.model'
import { Payment } from 'src/app/models/user/information/payment.model'


@Injectable({ providedIn: 'root' })
export class UserService {
  getMainInfoUrl = Links.prefix+'/v2/api/user/information';
  getAvatarsUrl = Links.prefix+'/v2/api/user/avatars';
  getCartUrl = Links.prefix+'/v2/api/user/carts';
  getScoreUrl = Links.prefix+'/v2/api/user/scores';
  getProfileUrl = Links.prefix+'/v2/api/user/profile';
  getAddressUrl = Links.prefix+'/v2/api/user/address';
  getShipmentUrl = Links.prefix+'/v2/api/user/shipment';
  getPaymentUrl = Links.prefix+'/v2/api/user/payment';

  constructor(private http: HttpClient) {}

  GetMainInformation() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<MainUserInformation>(this.getMainInfoUrl , httpOptions);
    } else {
      return this.http.get<MainUserInformation>(this.getMainInfoUrl);
    }

  }

  GetShipmentInformation() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<ShipmentInformation>(this.getShipmentUrl , httpOptions);
    } else {
      return this.http.get<ShipmentInformation>(this.getShipmentUrl);
    }

  }

  GetPaymentInformation() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<Payment[]>(this.getPaymentUrl , httpOptions);
    } else {
      return this.http.get<Payment[]>(this.getPaymentUrl);
    }

  }

  GetAddress() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<Address>(this.getAddressUrl , httpOptions);
    } else {
      return this.http.get<Address>(this.getAddressUrl);
    }

  }

  GetEditableInformation() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<EditUserInformation>(this.getProfileUrl , httpOptions);
    } else {
      return this.http.get<EditUserInformation>(this.getProfileUrl);
    }

  }

  SetEditableInformation(editObject) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.post(this.getProfileUrl ,editObject, httpOptions);
    } else {
      return this.http.post(this.getProfileUrl,editObject);
    }

  }

  SetShipmentInformation(shipmentObject) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.post(this.getShipmentUrl ,shipmentObject, httpOptions);
    } else {
      return this.http.post(this.getShipmentUrl,shipmentObject);
    }

  }

  GetAvatars() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<Avatar[]>(this.getAvatarsUrl , httpOptions);
    } else {
      return this.http.get<Avatar[]>(this.getAvatarsUrl);
    }

  }

  GetScores() {
    return this.http.get<Score[]>(this.getScoreUrl);
  }

  SaveAvatar(avatarObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.post(this.getAvatarsUrl , avatarObj,httpOptions);
    } else {
      return this.http.post(this.getAvatarsUrl , avatarObj);
    }

  }

  DeleteOrder(orderObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.put(this.getCartUrl , orderObj,httpOptions);
    } else {
      return this.http.put(this.getCartUrl , orderObj);
    }

  }

  AddOrder(auctionObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.post(this.getCartUrl , auctionObj,httpOptions);
    } else {
      return this.http.post(this.getCartUrl , auctionObj);
    }

  }

  GetShoppingCarts() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<Cart[]>(this.getCartUrl , httpOptions);
    } else {
      return this.http.get<Cart[]>(this.getCartUrl);
    }

  }

}
