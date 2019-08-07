import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Shop } from '../models/shop/shop.model';
import { Links } from '../links.component';
import { MainUserInformation } from '../models/user/information/main.model';
import { Cart } from '../models/user/information/cart.model';
import { Score } from '../models/user/information/score.model';
import { Avatar } from '../models/user/avatar.model';
import { EditUserInformation } from 'src/app/models/user/information/edit.model';
import { ShipmentInformation } from 'src/app/models/user/information/shipment.model';
import { Address } from 'src/app/models/user/information/address.model';
import { PaymentInfo } from 'src/app/models/user/information/paymentInfo.model';
import { UserCoupon } from 'src/app/models/user/userCoupon.model';
import { ShipmentMethod } from 'src/app/models/shipmentMethod.model';
import { SharingService } from 'src/app/services/sharing.service';
import { FavAuction } from '../models/auction/favorite.model';
import { GetTransactions } from '../models/service/getTransactions.model';
import { GetNotifications } from '../models/service/getNotifications.model';
import { GetMessages } from '../models/service/getMessages.model';


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
  couponUrl = Links.prefix+'/v2/api/user/coupons';
  shipmentMethodsUrl = Links.prefix+'/v2/api/user/shipment/methods';
  favoriteUrl = Links.prefix+'/v2/api/user/favorite';
  transactionsUrl = Links.prefix+'/v2/api/user/transactions';
  notificationsUrl = Links.prefix+'/v2/api/user/notifications';
  messagesUrl = Links.prefix+'/v2/api/user/messages';

  constructor(private http: HttpClient,private shared:SharingService) {}

  hideProfile(){
    this.shared.toggleMenu.profile = false;
    this.shared.toggleMenu.profileReset();
    this.shared.lastClass = "myCfnAnimation-fadeIn";
  }

  GetMessages(moreObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      return this.http.get<GetMessages>(this.messagesUrl,{ params: moreObj,
        headers: new HttpHeaders(
          {
            Authorization: 'Bearer ' + token
          }
        )});
    } else {
      return this.http.get<GetMessages>(this.messagesUrl, {params: moreObj});
    }

  }

  SendMessage(msgObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.post(this.messagesUrl, msgObj, httpOptions);
    } else {
      return this.http.post(this.messagesUrl, msgObj);
    }

  }

  DeleteNotification(notifObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.patch(this.notificationsUrl, notifObj, httpOptions);
    } else {
      return this.http.patch(this.notificationsUrl, notifObj);
    }

  }

  MarkAsReadNotification(notifObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.put(this.notificationsUrl, notifObj, httpOptions);
    } else {
      return this.http.put(this.notificationsUrl, notifObj);
    }

  }

  GetNotifications(moreObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      return this.http.get<GetNotifications>(this.notificationsUrl,{ params: moreObj,
        headers: new HttpHeaders(
          {
            Authorization: 'Bearer ' + token
          }
        )});
    } else {
      return this.http.get<GetNotifications>(this.notificationsUrl, {params: moreObj});
    }

  }

  ApplyGem() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.post<GetTransactions>(this.transactionsUrl ,{},httpOptions);
    } else {
      return this.http.post<GetTransactions>(this.transactionsUrl,{});
    }

  }

  GetTransactions(moreObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      return this.http.get<GetTransactions>(this.transactionsUrl,{ params: moreObj,
        headers: new HttpHeaders(
          {
            Authorization: 'Bearer ' + token
          }
        )});
    } else {
      return this.http.get<GetTransactions>(this.transactionsUrl, {params: moreObj});
    }

  }

  GetFavAuctions() {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<FavAuction[]>(this.favoriteUrl, httpOptions);
    } else {
      return this.http.get<FavAuction[]>(this.favoriteUrl);
    }
  }

  GetShipmentMethods() {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<ShipmentMethod[]>(this.shipmentMethodsUrl, httpOptions);
    } else {
      return this.http.get<ShipmentMethod[]>(this.shipmentMethodsUrl);
    }
  }

  GetUserCoupon() {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.get<UserCoupon>(this.couponUrl, httpOptions);
    } else {
      return this.http.get<UserCoupon>(this.couponUrl);
    }

  }

  CheckCoupon(couponObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.put(this.couponUrl, couponObj, httpOptions);
    } else {
      return this.http.put(this.couponUrl, couponObj);
    }

  }

  ApplyCoupon(couponObj) {

    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.post(this.couponUrl, couponObj , httpOptions);
    } else {
      return this.http.post(this.couponUrl, couponObj);
    }

  }

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
      return this.http.get<PaymentInfo[]>(this.getPaymentUrl , httpOptions);
    } else {
      return this.http.get<PaymentInfo[]>(this.getPaymentUrl);
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
