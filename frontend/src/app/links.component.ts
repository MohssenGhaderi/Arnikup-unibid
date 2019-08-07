export class Links {
  public static prefix = "https://admin.unibid.ir/";
  // public static prefix = "http://127.0.0.1:9001/";
  public static chest (image) { return this.prefix + 'static/images/chests/' + image };
  public static avatar (image) { return this.prefix + 'static/images/avatars/' + image };
  public static auction (image) { return this.prefix + 'static/images/auctions/' + image };
  public static photo (image) { return this.prefix + 'static/images/photos/' + image };
  public static product (image) { return this.prefix + 'static/images/products/' + image };
  public static ad (image) { return this.prefix + 'static/images/ads/' + image };
  public static category (image) { return this.prefix + 'static/images/icons/category/' + image };
  public static auctionUrl (id) { return this.prefix+id };
}
