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

const config: SocketIoConfig = { url: 'http://dev.unibid.ir', options: {resource:'A/socket.io', 'force new connection': true} };
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
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    HttpClientModule,
    routing,
    SocketIoModule.forRoot(config),
    HttpClientModule,       // (Required) For share counts
    ShareModule,
    ShareButtonsModule
  ],
providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
