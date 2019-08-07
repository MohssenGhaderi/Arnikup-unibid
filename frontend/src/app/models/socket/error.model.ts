export class Error {
  status: number;
  reason: string;
  message: string;
  auctionId: number;
}

export class ErrorMessage {
  error:Error;
}
