import { Injectable , EventEmitter} from '@angular/core';
import { ToggleMenu } from 'src/app/models/toggleMenu.model'
import { Search } from 'src/app/models/search.model'
import { AutoBid } from 'src/app/models/auction/autobid.model'
import { Cart } from 'src/app/models/cart.model'

@Injectable({ providedIn: 'root' })
export class SharingService {
  searchChanged: EventEmitter<string> = new EventEmitter();
  cartStateChanged: EventEmitter<Cart> = new EventEmitter();
  socialCloser: EventEmitter<string> = new EventEmitter();
  socialStay: EventEmitter<string> = new EventEmitter();

  emitCartState(cart:Cart){
    this.cartStateChanged.emit(cart);
  }

  getCartStateEmitter() {
    return this.cartStateChanged;
  }

  emitSearchChanged(string) {
    this.searchChanged.emit(string);
  }

  getSearchChangedEmitter() {
    return this.searchChanged;
  }

  emitCloseSocial(string) {
    this.socialCloser.emit(string);
  }

  emitSocialStay(string) {
    this.socialStay.emit(string);
  }
  getSocialStayEmitter() {
    return this.socialStay;
  }

  getSocialCloserEmitter() {
    return this.socialCloser;
  }

  toggleMenu = new ToggleMenu();
  search = new Search();
  autobid = new AutoBid();
  lastClass = "myCfnAnimation-fadeIn";
  basketClass = "myCfnAnimation-slideright";
  visibleProfile = false;
  shop = false;
  extraBid = false;
  showConfirm = false;
  productDetails = false;
  cart;

  constructor() {}

}
