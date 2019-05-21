import {Coin} from './coin.model';
import {CheapGem} from './cheapGem.model';
import {ExpGem} from './expGem.model';
import {Chest} from './chest.model';
import {Avatar} from './avatar.model';

export class Shop {
  coins: Coin[];
  cheapGems: CheapGem[];
  expGems: ExpGem[];
  chest: Chest;
  avatars: Avatar[];
}
