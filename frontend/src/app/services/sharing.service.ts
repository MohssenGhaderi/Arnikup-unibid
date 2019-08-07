import { Injectable , EventEmitter} from '@angular/core';
import { ToggleMenu } from 'src/app/models/toggleMenu.model';
import { Search } from 'src/app/models/search.model';
import { AutoBid } from 'src/app/models/auction/autobid.model';
import { Cart } from 'src/app/models/cart.model';
import { State } from 'src/app/models/user/information/state.model';
import { UserCoupon } from 'src/app/models/user/userCoupon.model';
import { ShipmentMethod } from 'src/app/models/shipmentMethod.model';
import { ItemGaranty } from 'src/app/models/itemGaranty.model';
import { ExtraBidMessage } from 'src/app/models/auction/extra-bid-message.model';
import { Notification } from 'src/app/models/user/notification.model';

@Injectable({ providedIn: 'root' })
export class SharingService {
  searchChanged: EventEmitter<string> = new EventEmitter();
  cartStateChanged: EventEmitter<Cart> = new EventEmitter();
  socialCloser: EventEmitter<string> = new EventEmitter();
  socialStay: EventEmitter<string> = new EventEmitter();
  stateChanged: EventEmitter<State> = new EventEmitter();
  couponChanged: EventEmitter<UserCoupon> = new EventEmitter();
  scrollReached: EventEmitter<string> = new EventEmitter();
  shipmentMethodChanged: EventEmitter<ShipmentMethod> = new EventEmitter();
  ItemGarantyChanged: EventEmitter<ItemGaranty> = new EventEmitter();
  ItemGarantyClosed: EventEmitter<number> = new EventEmitter();
  ExtraBidsChanged: EventEmitter<ExtraBidMessage> = new EventEmitter();
  ExtraBidsError: EventEmitter<string> = new EventEmitter();
  DeleteLike: EventEmitter<number> = new EventEmitter();
  DeleteNotification: EventEmitter<Notification> = new EventEmitter();
  CloseMessageType: EventEmitter<string> = new EventEmitter();
  ChangeGuestMessageType: EventEmitter<string> = new EventEmitter();

  emitChangeGuestMessageType(messageType:string){
    this.ChangeGuestMessageType.emit(messageType);
  }

  emitCloseMessageType(messageType:string){
    this.CloseMessageType.emit(messageType);
  }

  emitDeleteNotification(notification:Notification){
    this.DeleteNotification.emit(notification);
  }

  emitDeleteLike(auctionId:number){
    this.DeleteLike.emit(auctionId);
  }

  emitExtraBidsError(error:string){
    this.ExtraBidsError.emit(error);
  }

  emitExtraBidsChanged(ebidm:ExtraBidMessage){
    this.ExtraBidsChanged.emit(ebidm);
  }

  emitItemGarantyClose(orderId:number){
    this.ItemGarantyClosed.emit(orderId);
  }

  emitItemGaranty(itemGaranty:ItemGaranty){
    this.ItemGarantyChanged.emit(itemGaranty);
  }

  emitShipmentMethod(shipmentMethod:ShipmentMethod){
    this.shipmentMethodChanged.emit(shipmentMethod);
  }

  emitScrollReached(message:string){
    this.scrollReached.emit(message);
  }

  emitUserCoupon(userCoupon:UserCoupon){
    this.couponChanged.emit(userCoupon);
  }

  emitState(state:State){
    this.stateChanged.emit(state);
  }

  emitCartState(cart:Cart){
    this.cartStateChanged.emit(cart);
  }

  emitSearchChanged(string) {
    this.searchChanged.emit(string);
  }

  emitCloseSocial(string) {
    this.socialCloser.emit(string);
  }

  emitSocialStay(string) {
    this.socialStay.emit(string);
  }

  getChangeGuestMessageTypeEmitter() {
    return this.ChangeGuestMessageType;
  }

  getCloseMessageTypeEmitter() {
    return this.CloseMessageType;
  }

  getDeleteNotificationEmitter() {
    return this.DeleteNotification;
  }

  getDeleteLikeEmitter() {
    return this.DeleteLike;
  }

  getExtraBidsErrorEmitter() {
    return this.ExtraBidsError;
  }

  getExtraBidsChangedEmitter() {
    return this.ExtraBidsChanged;
  }

  getItemGarantyCloseEmitter() {
    return this.ItemGarantyClosed;
  }

  getItemGarantyEmitter() {
    return this.ItemGarantyChanged;
  }

  getShipmentMethodEmitter() {
    return this.shipmentMethodChanged;
  }

  getScrollReachedEmitter() {
    return this.scrollReached;
  }

  getCouponEmitter() {
    return this.couponChanged;
  }

  getStateEmitter() {
    return this.stateChanged;
  }

  getCartStateEmitter() {
    return this.cartStateChanged;
  }

  getSearchChangedEmitter() {
    return this.searchChanged;
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
  extraBidUsed = false;
  showConfirm = false;
  productDetails = false;
  states = false;
  busyScroll = false;
  auctions = 0;
  allAuctions = 0;
  shipmentMethod = false;
  cart;
  checkoutInfo = {"garanties":Array<ItemGaranty>(),"method": null};

  constructor() {}

}
