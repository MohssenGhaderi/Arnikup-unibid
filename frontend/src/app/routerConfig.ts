import { Routes, RouterModule } from '@angular/router';
import { SigninComponent } from './components/auth/signin/signin.component';
import { SignupComponent } from './components/auth/signup/signup.component';
import { AuctionComponent } from './components/auction/auction.component';
import { DefaultComponent } from './components/default/default.component';
import { VerificationComponent } from './components/auth/verification/verification.component';
import { ForgetPasswordComponent } from './components/auth/forget-password/forget-password.component';
import { SearchComponent } from './components/search/search.component';
import { HeldComponent } from './components/held/held.component';

const appRoutes: Routes = [
  {
      path: 'auction/:id',
      component: AuctionComponent
  },
  {
      path: 'finished',
      component: HeldComponent
  },
  {
      path: 'search',
      component: SearchComponent
  },
  {
      path: 'signin',
      component: SigninComponent
  },
  {
      path: 'signup',
      component: SignupComponent
  },
  {
      path: 'forgot',
      component: ForgetPasswordComponent
  },
  {
    path: '',
    component: DefaultComponent
  },
  {
    path: 'verification',
    component: VerificationComponent
  },
  {
    path: '',
    pathMatch: 'full',
    redirectTo: '/default'
  }
];
export const routing = RouterModule.forRoot(appRoutes);
