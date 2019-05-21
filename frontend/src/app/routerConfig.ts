import { Routes, RouterModule } from '@angular/router';
import { SigninComponent } from './auth/signin/signin.component';
import { SignupComponent } from './auth/signup/signup.component';
import { ShopComponent } from './shop/shop.component';
import { DefaultComponent } from './default/default.component';
import { VerificationComponent } from './auth/verification/verification.component';

const appRoutes: Routes = [
  {
      path: 'shop',
      component: ShopComponent
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
