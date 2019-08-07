import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { SignupComponent } from './components/auth/signup/signup.component';
import { SigninComponent } from './components/auth/signin/signin.component';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { DefaultComponent } from './components/default/default.component';
import { VerificationComponent } from './components/auth/verification/verification.component';
import { VerificationInputKeyupDirective } from './directives/verification-input-keyup.directive';
import { routing } from './routerConfig';
import { AuctionItemComponent } from './components/auction/auctionItem/auctionItem.component';
import { AuctionListComponent } from './components/auction/auctionList/auctionList.component';
import { SliderComponent } from './components/slider/slider.component';
import { ShopComponent } from './components/shop/shop.component';
import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { ProgressComponent } from './components/progress/progress.component';
import { AuctionComponent } from './components/auction/auction.component';
import { AuctionHeaderComponent } from './components/auction/components/auction-header/auction-header.component';
import { AuctionDetailsComponent } from './components/auction/components/auction-details/auction-details.component';
import { AuctionParticipantsComponent } from './components/auction/components/auction-participants/auction-participants.component';
import { AuctionSliderComponent } from './components/auction/components/auction-slider/auction-slider.component';
import { AuctionFooterComponent } from './components/auction/components/auction-footer/auction-footer.component';
import { ProfileComponent } from './components/user/profile/profile.component';
import { ShoppingCardComponent } from './components/user/shopping-card/shopping-card.component';
import { FinanceComponent } from './components/user/finance/finance.component';
import { AvatarComponent } from './components/user/avatar/avatar.component';
import { ScoreComponent } from './components/user/score/score.component';
import { LoadingComponent } from './components/loading/loading.component';
import { ErrorComponent } from './components/error/error.component';
import { SuccessComponent } from './components/success/success.component';
import { EditUserComponent } from './components/user/edit/edit.component';
import { ShipmentPreviewComponent } from './components/user/checkout/shipment/preview/shipment-preview.component';
import { ShipmentEditComponent } from './components/user/checkout/shipment/edit/shipment-edit.component';
import { PaymentComponent } from './components/user/checkout/payment/payment.component';
import { ForgetPasswordComponent } from './components/auth/forget-password/forget-password.component';
import { ExtraBidComponent } from './components/auction/components/extra-bid/extra-bid.component';
import { SearchComponent } from './components/search/search.component';
import { SearchBoxComponent } from './components/search-box/search-box.component';
import { SlideComponent } from './components/slider/slide/slide.component';
import { ConfirmComponent } from './components/confirm/confirm.component';
import { CouponComponent } from './components/coupon/coupon.component';
import { ProductDetailsComponent } from './components/product-details/product-details.component';
import { ColorComponent } from './components/color/color.component';
import { CoinParticipateComponent } from './components/auction/coin-participate/coin-participate.component';
import { CartLoadingComponent } from './components/cart-loading/cart-loading.component';
import { GemParticipateComponent } from './components/auction/gem-participate/gem-participate.component';
import { ParticipatedComponent } from './components/auction/participated/participated.component';
import { PersianPipe } from './pipes/persian.pipe';
import { FinishedComponent } from './components/auction/finished/finished.component';
import { HeldComponent } from './components/held/held.component';
import { ShareModule } from '@ngx-share/core';
import { ShareButtonsModule } from '@ngx-share/buttons';
import { SocialComponent } from './components/social/social.component';
import { StatesComponent } from './components/user/checkout/shipment/states/states.component';
import { SmallStatesComponent } from './components/user/states/states.component';
import { CouponItemComponent } from './components/coupon-item/coupon-item.component';
import { ScrollEventModule } from 'ngx-scroll-event';
import { ShipmentMethodComponent } from './components/user/shipment-method/shipment-method.component';
import { ItemGarantyComponent } from './components/user/item-garanty/item-garanty.component';
import { CartItemComponent } from './components/user/shopping-card/cart-item/cart-item.component';
import { PaymentItemComponent } from './components/user/checkout/payment/payment-item/payment-item.component';
import { ShipmentMethodItemComponent } from './components/user/shipment-method/shipment-method-item/shipment-method-item.component';
import { AutoBidComponent } from './components/auction/auto-bid/auto-bid.component';
import { ShareAuctionComponent } from './components/auction/components/share-auction/share-auction.component';
import { FavoriteComponent } from './components/favorite/favorite.component';
import { FavoriteItemComponent } from './components/favorite/favorite-item/favorite-item.component';
import { PasswordComponent } from './components/user/password/password.component';
import { NotificationComponent } from './components/user/notification/notification.component';
import { NotificationItemComponent } from './components/user/notification/notification-item/notification-item.component';
import { TransactionComponent } from './components/user/transaction/transaction.component';
import { TransactionItemComponent } from './components/user/transaction/transaction-item/transaction-item.component';
import { MessagesComponent } from './components/user/messages/messages.component';
import { MessageArchiveComponent } from './components/user/messages/message-archive/message-archive.component';
import { MessageArchiveItemComponent } from './components/user/messages/message-archive/message-archive-item/message-archive-item.component';
import { MessageTypeComponent } from './components/user/messages/message-type/message-type.component';
import { ContactComponent } from './components/contact/contact.component';
import { RadioButtonComponent } from './components/radio-button/radio-button.component';

const config: SocketIoConfig = { url: 'https://admin.unibid.ir', options: {transports:['websocket']} };
// const config: SocketIoConfig = { url: 'http://127.0.0.1:9001', options: {resource:'A/socket.io', 'force new connection': true} };

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    AuctionItemComponent,
    AuctionListComponent,
    SignupComponent,
    SigninComponent,
    DefaultComponent,
    VerificationComponent,
    VerificationInputKeyupDirective,
    SliderComponent,
    ShopComponent,
    ProgressComponent,
    AuctionComponent,
    AuctionHeaderComponent,
    AuctionDetailsComponent,
    AuctionParticipantsComponent,
    AuctionSliderComponent,
    AuctionFooterComponent,
    ProfileComponent,
    ShoppingCardComponent,
    FinanceComponent,
    AvatarComponent,
    ScoreComponent,
    LoadingComponent,
    ErrorComponent,
    SuccessComponent,
    EditUserComponent,
    ShipmentPreviewComponent,
    ShipmentEditComponent,
    PaymentComponent,
    ForgetPasswordComponent,
    ExtraBidComponent,
    SearchComponent,
    SearchBoxComponent,
    SlideComponent,
    ConfirmComponent,
    CouponComponent,
    ProductDetailsComponent,
    ColorComponent,
    CoinParticipateComponent,
    CartLoadingComponent,
    GemParticipateComponent,
    ParticipatedComponent,
    PersianPipe,
    FinishedComponent,
    HeldComponent,
    SocialComponent,
    StatesComponent,
    SmallStatesComponent,
    CouponItemComponent,
    ShipmentMethodComponent,
    CartItemComponent,
    ItemGarantyComponent,
    PaymentItemComponent,
    ShipmentMethodItemComponent,
    AutoBidComponent,
    ShareAuctionComponent,
    FavoriteComponent,
    FavoriteItemComponent,
    PasswordComponent,
    NotificationComponent,
    NotificationItemComponent,
    TransactionComponent,
    TransactionItemComponent,
    MessagesComponent,
    MessageArchiveComponent,
    MessageArchiveItemComponent,
    MessageTypeComponent,
    ContactComponent,
    RadioButtonComponent,
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    HttpClientModule,
    routing,
    SocketIoModule.forRoot(config),
    HttpClientModule,       // (Required) For share counts
    ShareModule,
    ShareButtonsModule,
    ScrollEventModule
  ],
providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
