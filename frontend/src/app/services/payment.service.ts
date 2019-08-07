import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Links } from '../links.component';
import { Payment } from '../models/payment.model';
import { ShipmentMethod } from '../models/shipmentMethod.model';

@Injectable({ providedIn: 'root' })
export class PaymentServices {

  buyCoinUrl = Links.prefix+'v2/api/buy/coin';
  buyGemUrl = Links.prefix+'v2/api/buy/gem';
  buyChestUrl = Links.prefix+'v2/api/buy/chest';
  buyProductUrl = Links.prefix+'v2/api/buy/product';
  paymentGatewayURL = Links.prefix+'v2/api/payment/zarinpal/gateway';

  constructor(private http: HttpClient) { }

  BuyProduct() {
    const headers = new HttpHeaders();
    const currentUser = localStorage.getItem('currentUser');
    let httpOptions = null;
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      httpOptions = {
        headers: new HttpHeaders({
          Authorization: 'Bearer ' + token
        })
      };
      return this.http.post<Payment>(this.buyProductUrl , httpOptions);
    }else{
      return this.http.post<Payment>(this.buyProductUrl , httpOptions);
    }
  }

  PaymentGateway(paymentObj) {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          'Authorization':`Bearer ${token}`
        })
      };
      return this.http.post<Payment>(this.paymentGatewayURL ,paymentObj, httpOptions);
    }else{
      return this.http.post<Payment>(this.paymentGatewayURL ,paymentObj);
    }
  }

  BuyCoin(coinObj) {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          'Authorization':`Bearer ${token}`
        })
      };
      return this.http.post<Payment>(this.buyCoinUrl ,coinObj, httpOptions);
    }else{
      return this.http.post<Payment>(this.buyCoinUrl ,coinObj);
    }
  }

  BuyGem(gemObj) {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          'Authorization':`Bearer ${token}`
        })
      };
      return this.http.post<Payment>(this.buyGemUrl ,gemObj, httpOptions);
    }else{
      return this.http.post<Payment>(this.buyGemUrl ,gemObj);
    }
  }

  BuyChest(chestObj) {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      const token = JSON.parse(currentUser)['accessToken'];
      const httpOptions = {
        headers: new HttpHeaders({
          'Authorization':`Bearer ${token}`
        })
      };
      return this.http.post<Payment>(this.buyChestUrl ,chestObj, httpOptions);
    }else{
      return this.http.post<Payment>(this.buyChestUrl ,chestObj);
    }
  }

}
