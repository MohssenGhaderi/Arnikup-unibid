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
import { SwiperModule } from 'angular2-useful-swiper';
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
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    HttpClientModule,
    routing,
    SwiperModule,
    SocketIoModule.forRoot(config)
  ],
providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
