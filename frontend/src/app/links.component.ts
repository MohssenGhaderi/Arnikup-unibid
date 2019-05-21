export class Links {
  // public static prefix = "http://dev.unibid.ir/";
  public static prefix = "http://127.0.0.1:9001/";
  public static chest (image) { return this.prefix + 'static/images/chests/' + image };
  public static avatar (image) { return this.prefix + 'static/images/avatars/' + image };
  public static product (image) { return this.prefix + 'static/images/products/' + image };
  public static category (image) { return this.prefix + 'static/images/icons/category/' + image };
}
