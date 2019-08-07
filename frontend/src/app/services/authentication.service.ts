import { Injectable } from '@angular/core';
import { HttpClient , HttpHeaders} from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { VerificationGet } from '../models/auth/verificationGet';
import { VerificationPut } from '../models/auth/verificationPut';
import { Links } from '../links.component';


@Injectable({ providedIn: 'root' })
export class AuthenticationService {
    // private currentUserSubject: BehaviorSubject<User>;
    // public currentUser: Observable<User>;
    avatarUrl = Links.prefix+'v2/api/auth/avatar';
    loginUrl = Links.prefix+'v2/api/auth/login';
    registerUrl = Links.prefix+'v2/api/auth/register';
    logoutUrl = Links.prefix+'v2/api/auth/logout';
    forgotUrl = Links.prefix+'v2/api/auth/password/forgot';
    verificationUrl = Links.prefix+'v2/api/auth/verify';
    passwordUrl = Links.prefix+'v2/api/auth/password/change';

    constructor(private http: HttpClient) {
        // this.currentUserSubject = new BehaviorSubject<User>(JSON.parse(localStorage.getItem('currentUser')));
        // this.currentUser = this.currentUserSubject.asObservable();
    }

    // public get currentUserValue(): User {
    //     return this.currentUserSubject.value;
    // }

    getAvatar(){
      return this.http.get(this.avatarUrl);
    }

    changePassword(changeObj) {

      const currentUser = localStorage.getItem('currentUser');
      if (currentUser) {
        const token = JSON.parse(currentUser)['accessToken'];
        const httpOptions = {
          headers: new HttpHeaders({
            Authorization: 'Bearer ' + token
          })
        };
        return this.http.post(this.passwordUrl, changeObj , httpOptions);
      } else {
        return this.http.post(this.passwordUrl, changeObj);
      }

    }

    forgotPassword(forgotObj) {
        return this.http.post(this.forgotUrl,forgotObj);
    }

    login(username: string, password: string) {
        return this.http.post(this.loginUrl, { username, password });
    }

    register(username: string, password: string, confirmPassword: string, mobile: string, invitor: string) {
      mobile = '0' + mobile.toString();
      let registerObj;
      if (invitor !== '') {
        registerObj = {
          username,
          password,
          confirmPassword,
          mobile,
          invitor
        };
      } else {
        registerObj = {
          username,
          password,
          confirmPassword,
          mobile
        };
      }
      return this.http.post(this.registerUrl, registerObj);
    }

    verifyGet() {
      return this.http.get<VerificationGet>(this.verificationUrl);
    }

    verifyPut(verifyPutObj) {
      return this.http.put<VerificationPut>(this.verificationUrl, verifyPutObj);
    }

    verifyPost(verifyPostObj) {
      return this.http.post(this.verificationUrl, verifyPostObj);
    }

    logout() {

        const currentUser = localStorage.getItem('currentUser');
        if (currentUser) {
          const token = JSON.parse(currentUser)['accessToken'];
          const httpOptions = {
            headers: new HttpHeaders({
              'Authorization':`Bearer ${token}`
            })
          };
          localStorage.removeItem('currentUser');
          return this.http.post(this.logoutUrl ,httpOptions);
        }
    }
}
