import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { SignupComponent } from './auth/signup/signup.component';
import { SigninComponent } from './auth/signin/signin.component';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { DefaultComponent } from './default/default.component';
import { VerificationComponent } from './auth/verification/verification.component';
import { VerificationInputKeyupDirective } from './directives/verification-input-keyup.directive';
import { routing } from './routerConfig';
import { AuctionItemComponent } from './auction/auctionItem/auctionItem.component';
import { AuctionListComponent } from './auction/auctionList/auctionList.component';
import { SwiperModule } from 'angular2-useful-swiper';
import { SliderComponent } from './slider/slider.component';
import { ShopComponent } from './shop/shop.component';
import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { ProgressComponent } from './progress/progress.component';

const config: SocketIoConfig = { url: 'http://127.0.0.1:9001', options: {} };

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
